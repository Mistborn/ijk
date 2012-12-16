$ ->
    YEAR = 1000 * 60 * 60 * 24 * 365.25
    # datoj
    $.datepicker.setDefaults
        dateFormat: 'yy-mm-dd'
        autoSize: true
        currentText: 'hodiaŭ'
        gotoCurrent: true
        hideIfNoPrevNextType: true
        showOtherMonths: true
        selectOtherMonths: true
        showButtonPanel: false
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
        changeMonth: true
        changeYear: true
        defaultDate: new Date window.KOMENCA_DATO - YEAR*25
        yearRange: "c-74:c+19"
            
        # new Date 2003, 7, 19

    liveri_aghon_lau_naskightago = (dato) ->
        (window.KOMENCA_DATO - dato) / YEAR

    # kalkulado de kotizoj dum aliĝo
    iso_to_date = (s) ->
        year = parseInt s[...4], 10
        month = parseInt(s[5...7], 10) - 1
        day = parseInt s[8...10], 10
        new Date year, month, day
    date_to_iso = (d) ->
        year = d.getYear() + 1900
        month = d.getMonth() + 1
        month = '0' + month if month < 10
        day = d.getDate()
        day = '0' + day if day < 10
        "#{year}-#{month}-#{day}"

    ekdato = -> iso_to_date $('#id_ekde').val()
    ghisdato = -> iso_to_date $('#id_ghis').val()
    naskighdato = -> iso_to_date $('#id_naskighdato').val()

    chu_plentempa = ->
        ekdato().getTime() is window.KOMENCA_DATO.getTime() and
            ghisdato().getTime() is window.FINIGHA_DATO.getTime()
    loghkategorio = -> $('#id_loghkategorio :selected').val()
    loghlando = -> $('#id_loghlando :selected').val()
    landokategorio = -> window.landoj[loghlando()]
    aghkategorio = ->
        agho = liveri_aghon_lau_naskightago naskighdato()
        result = null
        for limagho of window.limaghoj
            result = limagho if limagho > agho and
                (not result? or limagho < result)
        window.limaghoj[result]
    alighkategorio = -> # XXX supozante ke hodiaŭ estas la aliĝdato
        hodiau = date_to_iso new Date()
        result = null
        for limdato of window.limdatoj
            result = limdato if hodiau <= limdato and
                (not result? or limdato < result)
        return window.limdatoj[result]
    liveri_loghkoston = ->
        loghk = loghkategorio()
        return false if not loghk
        loghkosto_array = window.loghkategorioj[loghk]
        loghkosto = loghkosto_array?[if chu_plentempa() then 0 else 1]
    liveri_programkotizon = ->
        pk = window.programkotizoj
        aghk = aghkategorio()
        landok = landokategorio()
        alighk = alighkategorio()
        if not aghk? or not landok? or not alighk? then false
        else pk[aghk]?[landok]?[alighk]

    # dinama kalkulo de la kotizo
    kotizo = ->
        ###
        Liveri la bazan kotizon de tiu ĉi partoprenanto
        Formulo por kotizo:
            [manĝokosto laŭ la elekto] +
            [loĝkosto laŭ elekto kaj laŭ kvanto de tagoj] -
            [rabato pro UEA-membreco] + [program-kotizo]
        ###

        manghokosto = 0;
        $('input[name="manghomendoj"]:checked').each ->
            manghokosto += window.manghomendotipoj[$(this).val()]
        loghkosto = liveri_loghkoston()
        uearabato = if $('#id_chu_ueamembro').is(':checked')
            window.uearabatoj[landokategorio()]
        else 0
        programkotizo = liveri_programkotizon()
        eraroj = []
        eraroj.push 'manĝokosto nedefinita' if not manghokosto? 
        eraroj.push 'loĝkosto nedefinita' if not loghkosto? 
        eraroj.push 'programkotizo nedefinita' if not programkotizo? 
        eraroj.push 'uea-rabato nedefinita' if not uearabato?
        return "okazis eraro: #{eraroj.join ', '}.
            Bv kontakti la respondeculojn." if eraroj.length > 0
        klarigo = []
        klarigo.push "#{manghokosto}
            (manĝokosto)" if manghokosto or manghokosto is 0
        klarigo.push "#{loghkosto} (loĝkosto)" if loghkosto or loghkosto is 0
        klarigo.push "#{programkotizo}
            (programkotizo)" if programkotizo or programkotizo is 0
        if klarigo.length > 0
            klarigo = '(' + (klarigo.join ' + ') +
                (if uearabato then "- #{uearabato} (UEA-rabato)" else "") +
                ')'
        else klarigo = ''
        sumo = manghokosto + loghkosto + programkotizo - uearabato
        $('#informoj').text("Kotizo: #{sumo} #{klarigo}")

    kotizo_selectors = ['#id_naskighdato', '#id_loghlando',
        '#id_loghkategorio', 'input[name="manghomendoj"]',
        '#id_chu_ueamembro', '#id_ekde', '#id_ghis']
    $(kotizo_selectors.join ', ').change ->
        kotizo()
        #$('#informoj').text("Kotizo: #{kotizo()}")

    ### aspektigaj detaloj ###
    # montru la landokategorion malantaŭ la falmenuo post elekto de la lando
    # (kaj ne ene de la falmenuo)
    $('#id_loghlando option').each ->
        result = $(this).text().match /([^(]*)\(([^)]*)\)/
        return if not result?
        $(this).text result[1]
        $(this).data 'landokategorio', ' ' + result[2]
    $('#id_loghlando').after('<span class="klarigo"></span>').change ->
        $(this).next('.klarigo').text(
            $(this).find(':selected').data('landokategorio'))

    # montru nur-israelajn pagmanierojn nur se
    # la elektita lando estas Israelo
    $('#id_loghlando').change ->
        chu_israelo = $(this).find(
            ':selected').text().indexOf('Israelo') isnt -1
        $('input[name="pagmaniero"]').each ->
            $li = $($(this).parents('li')[0])
            if $li.is(':contains("nur en Israelo")')
                if chu_israelo then $li.show() else $li.hide()
