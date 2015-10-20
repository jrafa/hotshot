weekdays = ['Nd','Pn','Wt','Śr','Czw','Pt','So'];
months = ['Styczeń','Luty','Marzec','Kwiecień','Maj','Czerwiec','Lipiec','Sierpień','Wrzesień','Październik','Listopad','Grudzień'];

function calendar_translate(element) {
    $(element).attr('data-uk-datepicker',"{format:'DD.MM.YYYY', i18n: {weekdays: weekdays, months: months}}");
};

$(document).ready(function(){
    calendar_translate('#datepickerFrom');
    calendar_translate('#datepickerTo');
});
