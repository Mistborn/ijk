(function() {

  $(function() {
    var $tabs, DAY, YEAR, date_to_iso, iso_to_date, kotizo, kotizo_selectors, liveri_aghon_lau_naskightago, nav_callback;
    DAY = 1000 * 60 * 60 * 24;
    YEAR = DAY * 365.25;
    $.datepicker.setDefaults({
      dateFormat: 'yy-mm-dd',
      autoSize: true,
      currentText: 'hodiaŭ',
      gotoCurrent: true,
      hideIfNoPrevNextType: true,
      showOtherMonths: true,
      selectOtherMonths: true,
      showButtonPanel: false,
      changeMonth: false,
      changeYear: false,
      yearRange: "" + window.KOMENCJARO + ":" + window.KOMENCJARO,
      dayNames: ['dimanĉo', 'lundo', 'mardo', 'merkredo', 'ĵaŭdo', 'vendredo', 'sabato'],
      dayNamesMin: ['di', 'lu', 'ma', 'me', 'ĵa', 've', 'sa'],
      monthNames: ["januaro", "februaro", "marto", "aprilo", "majo", "junio", "julio", "aŭgusto", "septembro", "oktobro", "novembro", "decembro"],
      monthNamesShort: ["jan", "feb", "mar", "apr", "maj", "jun", "jul", "aŭg", "sep", "okt", "nov", "dec"]
    });
    $('#id_ekde').datepicker({
      defaultDate: window.KOMENCA_DATO,
      maxDate: window.FINIGHA_DATO
    });
    $('#id_ghis').datepicker({
      defaultDate: window.FINIGHA_DATO,
      minDate: window.KOMENCA_DATO
    });
    $('#id_naskighdato').datepicker({
      changeMonth: true,
      changeYear: true,
      defaultDate: new Date(window.KOMENCA_DATO - YEAR * 25),
      yearRange: "c-74:c+19"
    });
    liveri_aghon_lau_naskightago = function(dato) {
      if (dato) {
        return (window.KOMENCA_DATO - dato) / YEAR;
      } else {
        return dato;
      }
    };
    iso_to_date = function(s) {
      var day, month, year;
      if (s == null) return null;
      if (!s) return false;
      year = parseInt(s.slice(0, 4), 10);
      month = parseInt(s.slice(5, 7), 10) - 1;
      day = parseInt(s.slice(8, 10), 10);
      return new Date(year, month, day);
    };
    date_to_iso = function(d) {
      var day, month, year;
      if (d == null) return null;
      if (!d) return false;
      year = d.getYear() + 1900;
      month = d.getMonth() + 1;
      if (month < 10) month = '0' + month;
      day = d.getDate();
      if (day < 10) day = '0' + day;
      return "" + year + "-" + month + "-" + day;
    };
    window.partoprenelektoj = function() {
      var limagho, manghokosto, result, _ref, _ref2, _ref3, _ref4, _ref5, _ref6, _ref7,
        _this = this;
      this.ekdato = iso_to_date((_ref = $('#id_ekde').val()) != null ? _ref : false);
      this.ghisdato = iso_to_date((_ref2 = $('#id_ghis').val()) != null ? _ref2 : false);
      this.naskighdato = iso_to_date((_ref3 = $('#id_naskighdato').val()) != null ? _ref3 : false);
      this.chu_plentempa = this.ekdato === false ? null : this.ghisdato === false ? null : this.ekdato.getTime() === window.KOMENCA_DATO.getTime() && this.ghisdato.getTime() === window.FINIGHA_DATO.getTime();
      this.loghkategorio = (_ref4 = $('input[name="loghkategorio"]:checked').val()) != null ? _ref4 : false;
      this.loghlando = (_ref5 = $('#id_loghlando :selected').val()) != null ? _ref5 : false;
      this.landokategorio = !this.loghlando ? false : window.landoj[this.loghlando];
      this.agho = liveri_aghon_lau_naskightago(this.naskighdato);
      this.aghkategoriaj_informoj = (function() {
        if (!this.agho) {
          return this.agho;
        } else {
          result = null;
          for (limagho in window.limaghoj) {
            if (!(limagho < this.agho || ((result != null) && limagho > result))) {
              result = limagho;
            }
          }
          return window.limaghoj[result];
        }
      }).call(this);
      this.aghkategorio = this.aghkategoriaj_informoj ? this.aghkategoriaj_informoj[0] : this.aghkategoriaj_informoj;
      this.aghaldona_pago = this.aghkategoriaj_informoj ? this.aghkategoriaj_informoj[1] : this.aghkategoriaj_informoj;
      this.alighkategorio = (function() {
        var hodiau, limdato;
        hodiau = date_to_iso(new Date());
        result = null;
        for (limdato in window.limdatoj) {
          if (!(hodiau > limdato || ((result != null) && limdato > result))) {
            result = limdato;
          }
        }
        return window.limdatoj[result];
      })();
      this.tranoktoj = Math.floor((this.ghisdato - this.ekdato) / DAY);
      this.loghkosto = (function() {
        var base, _ref6;
        if (!(_this.loghkategorio !== false && (_this.chu_plentempa != null))) {
          return false;
        }
        base = (_ref6 = window.loghkategorioj[_this.loghkategorio]) != null ? _ref6[_this.chu_plentempa ? 0 : 1] : void 0;
        if (_this.chu_plentempa) {
          return base;
        } else {
          return base * _this.tranoktoj;
        }
      })();
      this.programkotizo = !((this.aghkategorio != null) && (this.landokategorio != null) && (this.alighkategorio != null)) ? null : this.aghkategorio === false || this.landokategorio === false || this.alighkategorio === false ? false : (_ref6 = window.programkotizoj[this.aghkategorio]) != null ? (_ref7 = _ref6[this.landokategorio]) != null ? _ref7[this.alighkategorio] : void 0 : void 0;
      manghokosto = 0;
      $('input[name="manghomendoj"]:checked').each(function() {
        return manghokosto += window.manghomendotipoj[$(this).val()];
      });
      this.manghokosto = isNaN(manghokosto) ? null : manghokosto;
      this.uearabato = !$('#id_chu_ueamembro').is(':checked') ? 0 : this.landokategorio != null ? window.uearabatoj[this.landokategorio] : null;
      this.chu_invitletero = $('#id_chu_bezonas_invitleteron').is(':checked');
      return this.chu_ekskurso = $('#id_chu_tuttaga_ekskurso').is(':checked');
    };
    kotizo = function() {
      /*
              Liveri la bazan kotizon de tiu ĉi partoprenanto
              Formulo por kotizo:
                  [manĝokosto laŭ la elekto] +
                  [loĝkosto laŭ elekto kaj laŭ kvanto de tagoj] -
                  [rabato pro UEA-membreco] + [program-kotizo]
      */
      var elektote, info, klarigo, klarigo_text, kosto, programkotizo, whatfor;
      info = new partoprenelektoj;
      klarigo = [];
      kosto = 0;
      if (info.manghokosto != null) {
        klarigo.push("" + info.manghokosto + " (manĝokosto)");
        kosto += info.manghokosto;
      } else {
        klarigo.push('(manĝokosto nedefinita)');
      }
      if (info.loghkosto === false) {
        klarigo.push('(elektu loĝkategorion)');
      } else if (info.loghkosto != null) {
        kosto += info.loghkosto;
        klarigo_text = info.chu_plentempa ? 'plentempa loĝkosto' : "loĝkosto por " + info.tranoktoj + " noktoj";
        klarigo.push("" + info.loghkosto + " (" + klarigo_text + ")");
      } else {
        klarigo.push('(loĝkosto nedefinita)');
      }
      if (info.programkotizo === false) {
        elektote = [];
        if (info.naskighdato === false) elektote.push('naskiĝdaton');
        if (info.landokategorio === false) elektote.push('loĝlandon');
        klarigo.push("(elektu " + (elektote.join(' kaj ')) + "            por kalkuli la programkotizon)");
      } else if (info.programkotizo != null) {
        whatfor = 'programkotizo';
        programkotizo = info.chu_plentempa ? info.programkotizo : (whatfor += " por " + (info.tranoktoj + 1) + " tagoj", info.programkotizo / 5 * (info.tranoktoj + 1));
        klarigo.push("" + programkotizo + " (" + whatfor + ")");
        kosto += programkotizo;
      } else {
        klarigo.push('(programkotizo nedefinita)');
      }
      if (info.chu_ekskurso) {
        kosto += window.krompagtipoj.ekskurso;
        klarigo.push("" + window.krompagtipoj.ekskurso + " (tut-taga ekskurso)");
      }
      if (info.chu_invitletero) {
        kosto += window.krompagtipoj.invitletero;
        klarigo.push("" + window.krompagtipoj.invitletero + " (invitletero)");
      }
      if (info.uearabato != null) kosto -= info.uearabato;
      klarigo = '[konsistas el ' + (klarigo.join(' + '));
      if (info.uearabato > 0) klarigo += " - " + info.uearabato + " (UEA-rabato)";
      if (info.uearabato == null) klarigo += ' (UEA-rabato nedefinita)';
      klarigo += ']';
      return $('#informoj').text("Kotizo: " + kosto + " " + klarigo);
    };
    kotizo_selectors = ['#id_naskighdato', '#id_loghlando', 'input[name="loghkategorio"]', 'input[name="manghomendoj"]', '#id_chu_ueamembro', '#id_ekde', '#id_ghis', '#id_chu_bezonas_invitleteron', '#id_chu_tuttaga_ekskurso'];
    $(kotizo_selectors.join(', ')).change(function() {
      return kotizo();
    });
    /* aspektigaj detaloj
    */
    $('#id_loghlando option').each(function() {
      var result;
      result = $(this).text().match(/([^(]*)\(([^)]*)\)/);
      if (!(result != null)) return;
      $(this).text(result[1]);
      return $(this).data('landokategorio', " " + result[2]);
    });
    $('#id_loghlando').after('<span class="klarigo"></span>').change(function() {
      return $(this).next('.klarigo').text($(this).find(':selected').data('landokategorio'));
    });
    $('#id_loghlando').change(function() {
      var chu_israelo;
      chu_israelo = $(this).find(':selected').text().indexOf('Israelo') !== -1;
      return $('input[name="pagmaniero"]').each(function() {
        var $li;
        $li = $($(this).parents('li')[0]);
        if ($li.is(':contains("nur en Israelo")')) {
          if (chu_israelo) {
            return $li.show();
          } else {
            $(this).prop('checked', false);
            return $li.hide();
          }
        }
      });
    });
    $tabs = $('#form-tabs').tabs();
    nav_callback = function(offset) {
      return function() {
        var active, newtab;
        active = $tabs.tabs('option', 'active');
        newtab = active + offset;
        if (newtab < 0 || newtab > 3) return false;
        $tabs.tabs('option', 'active', newtab);
        return false;
      };
    };
    $('.reen, .antauen, input[type="submit"]').button();
    $('.reen').click(nav_callback(-1));
    return $('.antauen').click(nav_callback(1));
  });

}).call(this);