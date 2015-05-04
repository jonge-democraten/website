jQuery(function($) {
    $(document).ready(function () {
        $('#event-calendar').fullCalendar({
            header: {
                left: 'prev,next today',
                center: 'title',
                right: 'month,agendaWeek'
            },

            defaultDate: window.__calendar_default_date,
            editable: false,
            eventLimit: true,
            timezone: "local",
            eventSources: [
                {
                    url: window.__calendar_events_url,
                    type: 'GET',
                    data: {},
                    error: function() {
                        $('#calendar-error').show();
                    }
                }
            ],
            loading: function(loading) {
                $('#calendar-loading').toggle(loading);
            }
        });
    });
});

