(function() {

  $(function() {
    var YEAR, aghkategorio, alighkategorio, chu_plentempa, date_to_iso, ekdato, ghisdato, iso_to_date, kotizo, kotizo_selectors, landokategorio, liveri_aghon_lau_naskightago, liveri_loghkoston, liveri_programkotizon, loghkategorio, loghlando, naskighdato;
    YEAR = 1000 * 60 * 60 * 24 * 365.25;
    $.datepicker.setDefaults({
      dateFormat: 'yy-mm-dd',
      autoSize: true,
      currentText: 'hodiaŭ',
      gotoCurrent: true,
      hideIfNoPrevNextType: true,
      showOtherMonths: true,
      selectOtherMonths: true,
      showButtonPanel: false,
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
      return (window.KOMENCA_DATO - dato) / YEAR;
    };
    iso_to_date = function(s) {
      var day, month, year;
      year = parseInt(s.slice(0, 4), 10);
      month = parseInt(s.slice(5, 7), 10) - 1;
      day = parseInt(s.slice(8, 10), 10);
      return new Date(year, month, day);
    };
    date_to_iso = function(d) {
      var day, month, year;
      year = d.getYear() + 1900;
      month = d.getMonth() + 1;
      if (month < 10) month = '0' + month;
      day = d.getDate();
      if (day < 10) day = '0' + day;
      return "" + year + "-" + month + "-" + day;
    };
    ekdato = function() {
      return iso_to_date($('#id_ekde').val());
    };
    ghisdato = function() {
      return iso_to_date($('#id_ghis').val());
    };
    naskighdato = function() {
      return iso_to_date($('#id_naskighdato').val());
    };
    chu_plentempa = function() {
      return ekdato().getTime() === window.KOMENCA_DATO.getTime() && ghisdato().getTime() === window.FINIGHA_DATO.getTime();
    };
    loghkategorio = function() {
      return $('#id_loghkategorio :selected').val();
    };
    loghlando = function() {
      return $('#id_loghlando :selected').val();
    };
    landokategorio = function() {
      return window.landoj[loghlando()];
    };
    aghkategorio = function() {
      var agho, limagho, result;
      agho = liveri_aghon_lau_naskightago(naskighdato());
      result = null;
      for (limagho in window.limaghoj) {
        if (limagho > agho && (!(result != null) || limagho < result)) {
          result = limagho;
        }
      }
      return window.limaghoj[result];
    };
    alighkategorio = function() {
      var hodiau, limdato, result;
      hodiau = date_to_iso(new Date());
      result = null;
      for (limdato in window.limdatoj) {
        if (hodiau <= limdato && (!(result != null) || limdato < result)) {
          result = limdato;
        }
      }
      return window.limdatoj[result];
    };
    liveri_loghkoston = function() {
      var loghk, loghkosto, loghkosto_array;
      loghk = loghkategorio();
      if (!loghk) return false;
      loghkosto_array = window.loghkategorioj[loghk];
      return loghkosto = loghkosto_array != null ? loghkosto_array[chu_plentempa() ? 0 : 1] : void 0;
    };
    liveri_programkotizon = function() {
      var aghk, alighk, landok, pk, _ref, _ref2;
      pk = window.programkotizoj;
      aghk = aghkategorio();
      landok = landokategorio();
      alighk = alighkategorio();
      if (!(aghk != null) || !(landok != null) || !(alighk != null)) {
        return false;
      } else {
        return (_ref = pk[aghk]) != null ? (_ref2 = _ref[landok]) != null ? _ref2[alighk] : void 0 : void 0;
      }
    };
    kotizo = function() {
      /*
              Liveri la bazan kotizon de tiu ĉi partoprenanto
              Formulo por kotizo:
                  [manĝokosto laŭ la elekto] +
                  [loĝkosto laŭ elekto kaj laŭ kvanto de tagoj] -
                  [rabato pro UEA-membreco] + [program-kotizo]
      */
      var eraroj, klarigo, loghkosto, manghokosto, programkotizo, sumo, uearabato;
      manghokosto = 0;
      $('input[name="manghomendoj"]:checked').each(function() {
        return manghokosto += window.manghomendotipoj[$(this).val()];
      });
      loghkosto = liveri_loghkoston();
      uearabato = $('#id_chu_ueamembro').is(':checked') ? window.uearabatoj[landokategorio()] : 0;
      programkotizo = liveri_programkotizon();
      eraroj = [];
      if (!(manghokosto != null)) eraroj.push('manĝokosto nedefinita');
      if (!(loghkosto != null)) eraroj.push('loĝkosto nedefinita');
      if (!(programkotizo != null)) eraroj.push('programkotizo nedefinita');
      if (!(uearabato != null)) eraroj.push('uea-rabato nedefinita');
      if (eraroj.length > 0) {
        return "okazis eraro: " + (eraroj.join(', ')) + ".            Bv kontakti la respondeculojn.";
      }
      klarigo = [];
      if (manghokosto || manghokosto === 0) {
        klarigo.push("" + manghokosto + "            (manĝokosto)");
      }
      if (loghkosto || loghkosto === 0) {
        klarigo.push("" + loghkosto + " (loĝkosto)");
      }
      if (programkotizo || programkotizo === 0) {
        klarigo.push("" + programkotizo + "            (programkotizo)");
      }
      if (klarigo.length > 0) {
        klarigo = '(' + (klarigo.join(' + ')) + (uearabato ? "- " + uearabato + " (UEA-rabato)" : "") + ')';
      } else {
        klarigo = '';
      }
      sumo = manghokosto + loghkosto + programkotizo - uearabato;
      return $('#informoj').text("Kotizo: " + sumo + " " + klarigo);
    };
    kotizo_selectors = ['#id_naskighdato', '#id_loghlando', '#id_loghkategorio', 'input[name="manghomendoj"]', '#id_chu_ueamembro', '#id_ekde', '#id_ghis'];
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
      return $(this).data('landokategorio', ' ' + result[2]);
    });
    $('#id_loghlando').after('<span class="klarigo"></span>').change(function() {
      return $(this).next('.klarigo').text($(this).find(':selected').data('landokategorio'));
    });
    return $('#id_loghlando').change(function() {
      var chu_israelo;
      chu_israelo = $(this).find(':selected').text().indexOf('Israelo') !== -1;
      return $('input[name="pagmaniero"]').each(function() {
        var $li;
        $li = $($(this).parents('li')[0]);
        if ($li.is(':contains("nur en Israelo")')) {
          if (chu_israelo) {
            return $li.show();
          } else {
            return $li.hide();
          }
        }
      });
    });
  });

}).call(this);
