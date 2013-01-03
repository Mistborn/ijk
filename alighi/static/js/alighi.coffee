$ ->
    NUMTABS = 6   
    DAY = 1000 * 60 * 60 * 24
    YEAR = DAY * 365.25
    # datoj
    $.datepicker.setDefaults
        dateFormat: 'yy-mm-dd'
        autoSize: yes
        currentText: 'hodiaŭ'
        gotoCurrent: yes
        hideIfNoPrevNextType: yes
        showOtherMonths: yes
        selectOtherMonths: yes
        showButtonPanel: no
        changeMonth: no
        changeYear: no
        yearRange: "#{window.KOMENCJARO}:#{window.KOMENCJARO}"
        dayNames: ['dimanĉo', 'lundo', 'mardo', 'merkredo',
                   'ĵaŭdo', 'vendredo', 'sabato']
        dayNamesMin: ['di', 'lu', 'ma', 'me', 'ĵa', 've', 'sa']
        monthNames:  ["januaro", "februaro", "marto", "aprilo",
            "majo", "junio", "julio", "aŭgusto",
            "septembro", "oktobro", "novembro", "decembro"]
        monthNamesShort: ["jan", "feb", "mar", "apr", "maj", "jun",
            "jul", "aŭg", "sep", "okt", "nov", "dec"]
    $('#id_ekde').datepicker
        defaultDate: window.KOMENCA_DATO
        maxDate: window.FINIGHA_DATO
    $('#id_ghis').datepicker
        defaultDate: window.FINIGHA_DATO
        minDate: window.KOMENCA_DATO
    $('#id_naskighdato').datepicker
        changeMonth: yes
        changeYear: yes
        defaultDate: new Date window.KOMENCA_DATO - YEAR*25
        yearRange: "c-74:c+19"
            
        # new Date 2003, 7, 19

    liveri_aghon_lau_naskightago = (dato) ->
        if dato then (window.KOMENCA_DATO - dato) / YEAR else dato

    # kalkulado de kotizoj dum aliĝo
    iso_to_date = (s) ->
        return null unless s?
        return off if not s
        year = parseInt s[...4], 10
        month = parseInt(s[5...7], 10) - 1
        day = parseInt s[8...10], 10
        new Date year, month, day
    date_to_iso = (d) ->
        return null unless d?
        return off if not d
        year = d.getYear() + 1900
        month = d.getMonth() + 1
        month = '0' + month if month < 10
        day = d.getDate()
        day = '0' + day if day < 10
        "#{year}-#{month}-#{day}"

    partoprenelektoj = ->
        @ekdato = iso_to_date $('#id_ekde').val() ? off
        @ghisdato = iso_to_date $('#id_ghis').val() ? off
        @naskighdato = iso_to_date $('#id_naskighdato').val() ? off

        # chu_plentempa estas null kaj ne false se la ekdato au ghisdato
        # de la partoprenanto estas nedifinita
        @chu_plentempa = if @ekdato is off then null
        else if @ghisdato is off then null
        else @ekdato.getTime() is window.KOMENCA_DATO.getTime() and
            @ghisdato.getTime() is window.FINIGHA_DATO.getTime()

        @loghkategorio = $('input[name="loghkategorio"]:checked').val() ? off
        @loghlando = $('#id_loghlando :selected').val() ? off
        @landokategorio = if not @loghlando then off
        else window.landoj[@loghlando]
        @agho = liveri_aghon_lau_naskightago @naskighdato
        @aghkategoriaj_informoj = if not @agho then @agho
        else
            result = null
            for limagho of window.limaghoj
                result = limagho unless limagho < @agho or
                    (result? and limagho > result)
            window.limaghoj[result]
        @aghkategorio = if @aghkategoriaj_informoj
            @aghkategoriaj_informoj[0]
        else @aghkategoriaj_informoj
        @aghaldona_pago = if @aghkategoriaj_informoj
            @aghkategoriaj_informoj[1]
        else @aghkategoriaj_informoj
        @alighkategorio = do -> # XXX supozante ke hodiaŭ estas la aliĝdato
            hodiau = date_to_iso new Date()
            result = null
            for limdato of window.limdatoj
                result = limdato unless hodiau > limdato or
                    (result? and limdato > result)
            window.limdatoj[result]
        @tranoktoj = Math.floor((@ghisdato - @ekdato) / DAY)
        @loghkosto = do =>
            return off unless @loghkategorio isnt off and @chu_plentempa?
            base = window.loghkategorioj[@loghkategorio]?[if @chu_plentempa
            then 0 else 1]
            if @chu_plentempa then base
            else base * @tranoktoj
        @programkotizo = unless @aghkategorio? and @landokategorio? and
            @alighkategorio? then null
            else if @aghkategorio is off or
            @landokategorio is off or @alighkategorio is off then off
            else window.programkotizoj[@aghkategorio]?[@landokategorio]?[@alighkategorio]
        manghokosto = 0
        $('input[name="manghomendoj"]:checked').each ->
            manghokosto += window.manghomendotipoj[$(this).val()]
        @manghokosto = if isNaN manghokosto then null else manghokosto
        @uearabato = if not $('#id_chu_ueamembro').is(':checked') then 0
        else if @landokategorio? then window.uearabatoj[@landokategorio]
        else null
        @chu_invitletero = $('#id_chu_bezonas_invitleteron').is ':checked'
        @chu_ekskurso = $('#id_chu_tuttaga_ekskurso').is(':checked')


    # dinama kalkulo de la kotizo
    kotizo = ->
        ###
        Liveri la bazan kotizon de tiu ĉi partoprenanto
        Formulo por kotizo:
            [manĝokosto laŭ la elekto] +
            [loĝkosto laŭ elekto kaj laŭ kvanto de tagoj] -
            [rabato pro UEA-membreco] + [program-kotizo]
        ###

        info = new partoprenelektoj

        klarigo = []
        kosto = 0

        # manghokosto ne povas esti off
        if info.manghokosto?
            klarigo.push "#{info.manghokosto} (manĝokosto)"
            kosto += info.manghokosto
        else klarigo.push '(manĝokosto nedefinita)'

        if info.loghkosto is off
            klarigo.push '(elektu loĝkategorion)'
        else if info.loghkosto?
            kosto += info.loghkosto
            klarigo_text = if info.chu_plentempa then 'plentempa loĝkosto'
            else "loĝkosto por #{info.tranoktoj} noktoj"
            klarigo.push "#{info.loghkosto} (#{klarigo_text})"
        else
            klarigo.push '(loĝkosto nedefinita)'

        if info.programkotizo is off
            elektote = []
            elektote.push 'naskiĝdaton' if info.naskighdato is off
            elektote.push 'loĝlandon' if info.landokategorio is off
            klarigo.push "(elektu #{elektote.join ' kaj '}
            por kalkuli la programkotizon)"
        else if info.programkotizo?
            whatfor = 'programkotizo'
            programkotizo = if info.chu_plentempa
                info.programkotizo
            else
                whatfor += " por #{info.tranoktoj+1} tagoj"
                info.programkotizo / 5 * (info.tranoktoj + 1)
            klarigo.push "#{programkotizo} (#{whatfor})"
            kosto += programkotizo
        else
            klarigo.push '(programkotizo nedefinita)'

        if info.chu_ekskurso
            kosto += window.krompagtipoj.ekskurso
            klarigo.push "#{window.krompagtipoj.ekskurso} (tut-taga ekskurso)"
        if info.chu_invitletero
            kosto += window.krompagtipoj.invitletero
            klarigo.push "#{window.krompagtipoj.invitletero} (invitletero)"
            
        kosto -= info.uearabato if info.uearabato?
        
        klarigo = '[konsistas el ' + (klarigo.join ' + ')
        klarigo += " - #{info.uearabato} (UEA-rabato)" if info.uearabato > 0
        klarigo += ' (UEA-rabato nedefinita)' unless info.uearabato?
        klarigo += ']'
        $('#informoj').text("Kotizo: #{kosto} #{klarigo}")

    kotizo_selectors = ['#id_naskighdato', '#id_loghlando'
        'input[name="loghkategorio"]', 'input[name="manghomendoj"]'
        '#id_chu_ueamembro', '#id_ekde', '#id_ghis',
        '#id_chu_bezonas_invitleteron', '#id_chu_tuttaga_ekskurso']
    $(kotizo_selectors.join ', ').change ->
        kotizo()

    ### aspektigaj detaloj ###
    # montru la landokategorion malantaŭ la falmenuo post elekto de la lando
    # (kaj ne ene de la falmenuo)
    $('#id_loghlando option').each ->
        result = $(this).text().match /([^(]*)\(([^)]*)\)/
        return if not result?
        $(this).text result[1]
        $(this).data 'landokategorio', " #{result[2]}"
    $('#id_loghlando').after('<span class="klarigo helptext"></span>').change ->
        $(this).next('.helptext').text(
            $(this).find(':selected').data('landokategorio'))

    # montru nur-israelajn pagmanierojn nur se
    # la elektita lando estas Israelo
    $('#id_loghlando').change ->
        chu_israelo = $(this)
            .find(':selected').text().indexOf('Israelo') isnt -1
        $('input[name="pagmaniero"]').each ->
            $li = $($(this).parents('li')[0])
            if $li.is(':contains("nur en Israelo")')
                if chu_israelo then $li.show()
                else
                    $(this).prop 'checked', off
                    $li.hide()
    .change()

    # tabs
    $tabs = $('#form-tabs').tabs
        hide:
            effect: 'slide'
            direction: 'left'
        show:
            effect: 'slide'
            direction: 'right'
        beforeActivate:
            (e, ui) ->
                tabdiff = ui.newTab.index() - ui.oldTab.index()
                if Math.abs(tabdiff) is 1
                    slide_dirs = ['left', 'right']
                else
                    slide_dirs = ['up', 'up'] # ['down', 'up']
                [hide_dir, show_dir] = slide_dirs
                [hide_dir, show_dir] = [show_dir, hide_dir] if tabdiff < 0
                $tabs.tabs 'option'
                    hide:
                        effect: 'slide'
                        direction: hide_dir
                    show:
                        effect: 'slide'
                        direction: show_dir
                # alert "we are going to move to tab #{ui.newTab.index()} from #{ui.oldTab.index()}"
    nav_callback = (offset) -> ->
        active = $tabs.tabs 'option', 'active'
        newtab = active+offset
        return false if newtab < 0 or newtab >= NUMTABS
        $tabs.tabs 'option', 'active', newtab
        false 

    $('.reen, .antauen, input[type="submit"]').button()
    $('.reen').click nav_callback -1
    $('.antauen').click nav_callback 1
    
    # glitilo por elekti la gamon de datoj de partoprenado
    datogamo_start = window.KOMENCA_DATO.getDate()
    datogamo_end = window.FINIGHA_DATO.getDate()
    numnotches = datogamo_end - datogamo_start + 2
    curstart = if c = iso_to_date $('#id_ekde').val() then c.getDate() else datogamo_start
    curend = if c = iso_to_date $('#id_ghis').val() then c.getDate() else datogamo_end
    
    $('#id_ekde, #id_ghis').parent().hide()
    tabwidths = $('.tab').map -> $(this).width()
    tabwidth = Math.max tabwidths...
    widget_width = tabwidth - 300 - 14*2.5
    
    $datesliderli = $('<li class="required">
        <label for="id_datogamo">La daŭro de mia partopreno:</label></li>')
        .insertAfter $('#id_ghis').parent()
    $dateslider_container = $('<div></div>').appendTo($datesliderli)
        .width(widget_width)
    $gvidilo = $('<div id="datogamo-gvidilo"></div>').css
        width: widget_width
        margin: 'auto', padding: 0
        whiteSpace: 'nowrap';
    $.each [datogamo_start-1..datogamo_end+1], (i, v) ->
        $("<div class=\"datomarko\" id=\"id_datomarko_#{v}\">#{v}</div>")
            .css
                display: 'inline-block'
                width: "#{100 / numnotches}%"
                margin: 0, padding: 0
            .appendTo $gvidilo
    $dateslider_container.append $gvidilo
    $dateslider = $('<div class="datogamo" id="id_datogamo"></div>')
        .appendTo($dateslider_container)
        .css
            width: widget_width
            clear: 'both'
        .slider
            min: datogamo_start - 1
            max: datogamo_end + 1
            range: on
            values: [curstart, curend]
            change: (e, ui) ->
                #alert "event type is #{e.type}"
                [ekde, ghis] = ui.values 
                $('#id_ekde').val("2013-08-#{ekde}")
                $('#id_ghis').val("2013-08-#{ghis}")
                $('.datomarko').each ->
                    $(this).css fontWeight: 'normal'
                $("#id_datomarko_#{ekde}, #id_datomarko_#{ghis}").css 
                    fontWeight: 'bold'
    $dateslider.slider 'values', $dateslider.slider('values')
    $("<div>la oficiala daŭro de IJK estas de la #{datogamo_start}-a 
            ĝis la #{datogamo_end}-a de aŭgusto, 2013</div>")
        .appendTo($dateslider_container).css
            width: widget_width * (numnotches-2) / numnotches
            height: '1em'
            fontSize: '80%'
            borderTop: '3px dotted blue'
            margin: 0#'auto'
            position: 'relative'
            padding: 0
            left: widget_width / numnotches + 14
            color: 'blue'
            textAlign: 'center'
            

