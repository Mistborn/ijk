$ ->
    # datoj
    $.datepicker.setDefaults
        dateFormat: 'yy-dd-mm'
        dayNames: ['dimanĉo', 'lundo', 'mardo', 'merkredo',
                   'ĵaŭdo', 'vendredo', 'sabato']
        dayNamesMin: ['di', 'lu', 'ma', 'me', 'ĵa', 've', 'sa']
        monthNames:  ["januaro", "februaro", "marto", "aprilo",
            "majo", "junio", "julio", "aŭgusto",
            "septembro", "octobro", "novembero", "decembro"]
        monthNamesShort: ["jan", "feb", "mar", "apr", "maj", "jun",
            "jul", "aŭg", "sep", "oct", "nov", "dec"]
    $('#id_naskighdato, #id_ekde, #id_ghis').datepicker()

    liveri_aghon_lau_naskightago = (dato) ->
        (new Date(2013, 7, 19) - dato) / (1000*60*60*24*365.25)