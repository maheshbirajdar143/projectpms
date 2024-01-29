function highlightShot(button) 
                    {
                    var row = $(button).closest('tr');
                    $(row).find('td:eq(2)').addClass('highlight');
                    }

                function removeHighlight(button) 
                    {
                    var row = $(button).closest('tr');
                    $(row).find('td:eq(2)').removeClass('highlight');
                    }