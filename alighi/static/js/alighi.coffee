alighi_form = ->
    NUMTABS = 6   
    DAY = 1000 * 60 * 60 * 24
    YEAR = DAY * 365.25
    PROGRAMMINAGHO = 12
    LOGHMINAGHO = 5
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
        minDate: window.PLEJFRUA_DATO
        maxDate: window.FINIGHA_DATO
    $('#id_ghis').datepicker
        defaultDate: window.FINIGHA_DATO
        minDate: window.KOMENCA_DATO
        maxDate: window.PLEJMALFRUA_DATO
    $('#id_naskighdato').datepicker
        changeMonth: yes
        changeYear: yes
        defaultDate: new Date window.KOMENCA_DATO - YEAR*25
        yearRange: "-100:-2"
            
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

    window.partoprenelektoj = ->
        @ekdato = iso_to_date $('#id_ekde').val() ? off
        @ghisdato = iso_to_date $('#id_ghis').val() ? off
        @naskighdato = iso_to_date $('#id_naskighdato').val() ? off

        # chu_plentempa estas null kaj ne false se la ekdato au ghisdato
        # de la partoprenanto estas nedifinita
        @chu_plentempa = if @ekdato is off or @ghisdato is off then null
        else @ekdato.getTime() <= window.KOMENCA_DATO.getTime() and
            @ghisdato.getTime() >= window.FINIGHA_DATO.getTime()

        @loghkategorio = $('input[name="loghkategorio"]:checked').val() ? off
        @loghlando = $('#id_loghlando :selected').val() ? off
        @landokategorio = if not @loghlando then off
        else window.landoj[@loghlando]
        @agho = liveri_aghon_lau_naskightago @naskighdato
        @aghkategoriaj_informoj = if not @agho then @agho
        else
            result = null
            minimum = null
            for limagho of window.limaghoj
                result = limagho unless limagho < @agho or
                    (result? and limagho > result)
                minimum = limagho unless limagho > @agho or
                    (minimum? and limagho < minimum)
            window.limaghoj[result]
        @aghkategorio = if @aghkategoriaj_informoj
            @aghkategoriaj_informoj[0]
        else @aghkategoriaj_informoj
        @aghaldona_pago = if @aghkategoriaj_informoj
            @aghkategoriaj_informoj[1] * (1+Math.floor(@agho)-parseInt(minimum))
        else @aghkategoriaj_informoj
        ###
        @alighkategorio = do -> # XXX supozante ke hodiaŭ estas la aliĝdato
            hodiau = date_to_iso new Date()
            result = null
            for limdato of window.limdatoj
                result = limdato unless hodiau > limdato or
                    (result? and limdato > result)
            window.limdatoj[result]
        ###
        @alighkategorio = $('input[name="antaupagos_ghis"]:checked').val() ? off
        @alighlimdato = if @alighkategorio
            window.limdatoj[@alighkategorio] 
        else 
            off
        # unua kaj lasta tagoj de la dumkongresa partopreno:
        @unuatago = Math.max(@ekdato, window.KOMENCA_DATO)
        @lastatago = Math.min(@ghisdato, window.FINIGHA_DATO)
        # @tranoktoj estas la kvanto de tranoktoj dum la kongreso mem
        # kaj @superaj_tranoktoj estas la kvanto de tranokto 
        # antaŭ/post la kongreso
        @tranoktoj = Math.floor((@lastatago - @unuatago) / DAY)
        @superaj_tranoktoj = do =>
            antauaj = if @ekdato < @unuatago
                Math.floor (@unuatago - @ekdato) / DAY
            else 0
            postaj = if @ghisdato > @lastatago
                Math.floor (@ghisdato - @lastatago) / DAY
            else 0
            return antauaj + postaj
        @partoprentagoj = Math.floor((@lastatago - @unuatago) / DAY) + 1
        @relativa_partopreno = if @chu_plentempa then 1
        else (@partoprentagoj) / 5
        @manghorelativeco = if @chu_plentempa then 1
        else @partoprentagoj / 6
        @loghkosto = do =>
            return 0 if @agho isnt off and @agho < LOGHMINAGHO
            return off unless @loghkategorio isnt off and @chu_plentempa?
            return null unless window.loghkategorioj[@loghkategorio]?
            [@plentempa, @eksterkongresa] = window.loghkategorioj[@loghkategorio]
            # @plentempa estas la plena kosto de dumkongresa loĝado
            # @eksterkongresa estas la kosto de unu nokto eksterkongrese
            if @chu_plentempa
                return @plentempa + @superaj_tranoktoj * @eksterkongresa
            else
                return (@tranoktoj + @superaj_tranoktoj) * @eksterkongresa
        @programkotizo = if @agho isnt off and @agho < PROGRAMMINAGHO then 0
        else unless @aghkategorio? and @landokategorio? and 
            @alighkategorio? then null
        else if @aghkategorio is off or
            @landokategorio is off or @alighkategorio is off then off
        else window.programkotizoj[@aghkategorio]?[@landokategorio]?[@alighkategorio]
        @programkotizo *= @relativa_partopreno if @programkotizo
        if @programkotizo
            @programkotizo += if @aghaldona_pago then @aghaldona_pago else 0
        @chu_viando = do =>
            return null unless window.krompagtipoj.viando?
            tipo_id = $('[name="manghotipo"]:checked').attr 'id'
            tipo = $("label[for='#{tipo_id}']").text().toLowerCase()
            return -1 isnt tipo.indexOf 'viand'
        manghokosto = 0
        $('input[name="manghomendoj"]:checked').each ->
            manghokosto += window.manghomendotipoj[$(this).val()]
        @manghokosto = if isNaN manghokosto then null else manghokosto
        if @manghokosto
            @manghokosto += window.krompagtipoj.viando if @chu_viando
            @manghokosto *= @manghorelativeco 
        @uearabato = if not $('#id_chu_ueamembro').is(':checked') or
        not @programkotizo > 0 then 0
        else if @landokategorio? and @programkotizo > 0
            if @landokategorio isnt off
                window.uearabatoj[@landokategorio]
            else
                off
        else null
        @uearabato *= @relativa_partopreno if @uearabato
        @chu_invitletero = $('#id_chu_bezonas_invitleteron').is ':checked'
        @chu_ekskurso = $('#id_chu_tuttaga_ekskurso').is ':checked'

    # konstruo de la strukturo de la kotizo-"fakturo"
    $('#js-active').val(1)
    $('.fakturo-placeholder').addClass 'fakturo'
    $('.fakturo').append '<span class="label">Kotizo: </span>'
    $kotizoul = $('<ul></ul>').appendTo '.fakturo'
    kotizeroj = ['programo', 'loghado', 'mangho'
        'ekskurso', 'invitletero', 'uearabato', 'sumo']
    for id in kotizeroj
        signo = switch id
                when 'programo' then ''
                when 'uearabato' then '\u2013'
                when 'sumo' then '='
                else '+'
        $kotizoul.append "<li class='#{id}-li'>
            <div class='kotizo-signo #{id}-signo'>#{signo}</div>
            <div class='kotizo-ero #{id}-ero'>
                <div class='kotizo-kosto #{id}-kosto'></div>
                <div class='kotizo-klarigo #{id}-klarigo'></div>
            </div>
        </li>"
    $('.mangho-klarigo').text 'manĝado'
    # $('#loghado-klarigo').text 'loghado'
    $('.programo-klarigo').text 'programo'
    $('.ekskurso-klarigo').text 'ekskurso'
    $('.invitletero-klarigo').text 'invitletero'
    $('.uearabato-klarigo').text 'UEA-rabato'
    $('.sumo-klarigo').text 'sumo'
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

        # klarigo = []
        kosto = 0
        nedifinita = '(nedifinita)'
        elektu = '(elektu)'
        
        # manghokosto ne povas esti off
        if info.manghokosto?
            # klarigo.push "#{info.manghokosto} (manĝokosto)"
            # $('#mangho-klarigo').text('manĝokosto')
            $('.mangho-kosto').text info.manghokosto
            kosto += info.manghokosto
            if info.chu_viando
                $('.mangho-klarigo').text 'manĝado (viande)'
            else
                $('.mangho-klarigo').text 'manĝado'
        else
            $('.mangho-kosto').text nedifinita

        if info.loghkosto is off
            $('.loghado-kosto').text elektu
            $('.loghado-klarigo').text 'loĝado'
        else if info.loghkosto?
            kosto += info.loghkosto
            klarigo_text = do ->
                if info.chu_plentempa 
                    if info.superaj_tranoktoj is 0
                        return 'plentempa loĝado'
                    else if info.superaj_tranoktoj is 1
                        return "plentempa loĝado kaj aldona tranokto"
                    else
                        return "plentempa loĝado kaj #{info.superaj_tranoktoj} 
                                aldonaj tranoktoj"
                else "loĝado por #{info.tranoktoj + info.superaj_tranoktoj} 
                      noktoj"
            $('.loghado-kosto').text info.loghkosto
            $('.loghado-klarigo').text klarigo_text
        else
            $('.loghado-kosto').text nedifinita
            $('.loghado-klarigo').text 'loĝado'

        if info.programkotizo is off
            elektote = []
            elektote.push 'naskiĝdaton' if info.naskighdato is off
            elektote.push 'loĝlandon' if info.landokategorio is off
            elektote.push 'antaŭpagan daton' if info.alighkategorio is off
            $('.programo-kosto').text "(elektu #{elektote.join ' kaj '})"
            $('.programo-klarigo').text 'programo'
        else if info.programkotizo is 0
            klarigo = 'programo'
            $('.programo-klarigo').text klarigo
            $('.programo-kosto').text info.programkotizo
        else if info.programkotizo?
            klarigo = 'programo'
            if not info.chu_plentempa
                klarigo += " por #{info.partoprentagoj} tagoj"
            $('.programo-klarigo').text klarigo
            $('.programo-kosto').text info.programkotizo
            kosto += info.programkotizo
        else
            $('.programo-klarigo').text 'programo'
            $('.programo-kosto').text nedifinita

        if info.chu_ekskurso
            $('.ekskurso-li').show()
            kosto += window.krompagtipoj.ekskurso
            $('.ekskurso-kosto').text window.krompagtipoj.ekskurso
        else
            $('.ekskurso-li').hide()
        
        if info.chu_invitletero
            $('.invitletero-li').show()
            kosto += window.krompagtipoj.invitletero
            $('.invitletero-kosto').text window.krompagtipoj.invitletero
        else
            $('.invitletero-li').hide()

        if info.uearabato?
            if info.uearabato is off
                $('.uearabato-li').show()
                $('.uearabato-kosto').text '(elektu loĝlandon)'
            else if info.uearabato > 0
                kosto -= info.uearabato
                $('.uearabato-li').show()
                $('.uearabato-kosto').text info.uearabato
            else
                $('.uearabato-li').hide()
        else
            $('.uearabato-li').show()
            $('.uearabato-kosto').text nedifinita

        $('.sumo-kosto').text "#{kosto} €"
        $('#id_alighila_kotizo').val(kosto)
        
        #klarigo = '[konsistas el ' + (klarigo.join ' + ')
        #klarigo += " - #{info.uearabato} (UEA-rabato)" if info.uearabato > 0
        #klarigo += ' (UEA-rabato nedefinita)' unless info.uearabato?
        #klarigo += ']'
        #$('#kotizo').text("Kotizo: #{kosto} #{klarigo}")

    kotizo_selectors = ['#id_naskighdato', '#id_loghlando'
        'input[name="loghkategorio"]' 
        'input[name="manghomendoj"]', '[name="manghotipo"]'
        '#id_chu_ueamembro', '#id_ekde', '#id_ghis',
        '#id_chu_bezonas_invitleteron', '#id_chu_tuttaga_ekskurso'
        'input[name="antaupagos_ghis"]']
    for selector in kotizo_selectors
        $(selector).change kotizo

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
         
    nav_callback = (offset) -> ->
        active = $tabs.tabs 'option', 'active'
        newtab = active + offset
        if newtab >= NUMTABS
            $('body, html').animate scrollTop: $('.alighi').offset().top, 
                400, 'swing', ->
                    $('.alighi').effect 'highlight', color: 'red'
            return false
        return false if newtab < 0 or newtab >= NUMTABS
        $tabs.tabs 'option', 'active', newtab
        false

    $('.reen, .antauen, .alighi').button()
    $('.reen').click nav_callback -1
    $('.antauen').click nav_callback 1

    # tabs
    activate_cb = (e, ui) ->
        tab = ui.newTab ? ui.tab
        $('.reen').button 'option', 'disabled', tab.index() is 0
        # set the height back to auto and overflow to visible
        $(this).css 'height', 'auto'
        $(this).css 'overflow', 'visible'
    $tabs = $('#form-tabs').tabs
        hide:
            effect: 'slide'
            direction: 'left'
        show:
            effect: 'slide'
            direction: 'right'
        beforeActivate: (e, ui) ->
            # keep the height constant while transitioning
            $(this).css 'height', $(this).height()
            $(this).css 'overflow', 'hidden'
            
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
        activate: activate_cb
        create: activate_cb
    
    # glitilo por elekti la gamon de datoj de partoprenado
    kongreso_start = window.KOMENCA_DATO.getDate()
    kongreso_end = window.FINIGHA_DATO.getDate()
    datogamo_start = window.PLEJFRUA_DATO.getDate()
    datogamo_end = window.PLEJMALFRUA_DATO.getDate()
    numnotches = datogamo_end - datogamo_start
    curstart = if c = iso_to_date $('#id_ekde').val() then c.getDate()
    else kongreso_start
    curend = if c = iso_to_date $('#id_ghis').val() then c.getDate()
    else kongreso_end
    
    errorlist = []
    $('#id_ekde, #id_ghis').parent().hide()
    $('#id_ekde, #id_ghis').prevAll('.errorlist').find('li').each ->
        errorlist.push $(this).text()
    $newerrorlist = $('<ul class="errorlist"></ul>')
    $errorlis = for error in errorlist
        $("<li>#{error}</li>").appendTo $newerrorlist
    tabwidths = $('.tab').map -> $(this).width()
    tabwidth = Math.max $.makeArray(tabwidths)...
    widget_width = tabwidth - 300 - 14*6#2.5
    
    $datesliderli = $('<li class="required">
        <label for="id_datogamo">La daŭro de mia partopreno:</label></li>')
        .insertAfter $('#id_ghis').parent()
    $datesliderli.prepend $newerrorlist if $errorlis.length > 0
    $dateslider_container = $('<div></div>').appendTo($datesliderli)
        .width(widget_width)
    $gvidilo = $('<div id="datogamo-gvidilo"></div>').css
        width: widget_width
        margin: 'auto', padding: 0
        whiteSpace: 'nowrap';
    $.each [datogamo_start..datogamo_end], (i, v) ->
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
            #position: relative
            left: '8px'
        .slider
            min: datogamo_start
            max: datogamo_end
            range: on
            values: [curstart, curend]
            change: (e, ui) ->
                #alert "event type is #{e.type}"
                [ekde, ghis] = ui.values 
                $('#id_ekde').val("2013-08-#{ekde}").change()
                $('#id_ghis').val("2013-08-#{ghis}").change()
                $('.datomarko').each ->
                    $(this).css fontWeight: 'normal'
                $("#id_datomarko_#{ekde}, #id_datomarko_#{ghis}").css 
                    fontWeight: 'bold'
    $dateslider.slider 'values', $dateslider.slider('values')
    $("<div>la oficiala daŭro de IJK estas de la #{kongreso_start}-a 
            ĝis la #{kongreso_end}-a de aŭgusto, 2013</div>")
        .appendTo($dateslider_container).css
            width: widget_width*(kongreso_end - kongreso_start)/numnotches
            height: '1em'
            fontSize: '80%'
            borderTop: '3px dotted #2a3753'
            margin: 0#'auto'
            position: 'relative'
            padding: 0
            left: 14 + (kongreso_start - datogamo_start) * widget_width / numnotches
            color: '#2a3753'
            textAlign: 'center'
            fontWeight: 'bold'
            
    # ŝanĝu al la tab kun la unua eraro, se estas eraroj
    newtab = null
    $('.tab').each ->
        if $(this).find('.errorlist').length > 0
            id = $(this).attr('id')
            newtab = parseInt id[id.indexOf('-')+1..] unless newtab?
    if newtab? then $tabs.tabs 'option', 'active', newtab

    # avertu la uzanton, se li-ŝi provas foriri de la paĝo antaŭ ĝia alsendo
    onbeforeunload = (e) ->
        e.returnValue = 'Vi estas pleniganta la aliĝformularon por IJK. Se vi forlasas la paĝon, la informoj jam donitaj de vi perdiĝos!'
    $('input, select, textarea').change ->
        window.onbeforeunload = onbeforeunload
    $('#alighi-btn').click ->
        window.onbeforeunload = null
    if $('.button-error').length then window.onbeforeunload = onbeforeunload

$ ->
    alighi_form()
