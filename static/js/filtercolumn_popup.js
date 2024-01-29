document.addEventListener('DOMContentLoaded', function () {
    const table = document.getElementById('table');
    const headers = table.getElementsByTagName('th');
    const storedFilters = JSON.parse(sessionStorage.getItem('tableFilters')) || {};

    // Update filter symbols and apply stored filters
    for (let i = 1; i < headers.length - 1; i++) {
        const filterSymbol = document.createElement('span');
        filterSymbol.innerHTML = '<span style="font-size: smaller;">&#9660;</span>';
        filterSymbol.style.cursor = 'pointer';
        filterSymbol.onclick = function () {
            showFilterDropdown(i);
        };
        headers[i].innerHTML = headers[i].textContent;          // Clear existing content
        headers[i].appendChild(filterSymbol);

        // Check if a filter is applied to this header
        if (storedFilters[i] && storedFilters[i] !== 'all') {
            applyFilter(i, storedFilters[i]);
            // Highlight the filter symbol for this header
            highlightFilterSymbol(i, '#ffcc00');  // Change color to your preference
        }
    }

    function showFilterDropdown(columnIndex) {
        // Check if the dropdown is already open
        const existingDropdown = document.getElementById('filterDropdown');
        if (existingDropdown) {
            // Dropdown is open, close it
            document.body.removeChild(existingDropdown);
            return;
        }

        const values = Array.from(new Set(Array.from(table.rows).slice(1).map(row => row.cells[columnIndex].textContent)));
        const dropdown = document.createElement('select');
        dropdown.id = 'filterDropdown'; // Set an ID to easily identify the dropdown
        dropdown.innerHTML = '<option value="all" style="text-align:center">All</option>';

        // Modify to create a multiple selection dropdown
        dropdown.multiple = true;

        values.forEach(value => {
            const option = document.createElement('option');
            option.value = value;
            option.text = value;
            dropdown.add(option);
        });

        // Set selected values from stored filters
        if (storedFilters[columnIndex] && storedFilters[columnIndex] !== 'all') {
            const selectedValues = storedFilters[columnIndex].split(',');
            Array.from(dropdown.options).forEach(option => {
                option.selected = selectedValues.includes(option.value);
            });
        }

        dropdown.onchange = function () {
            const selectedOptions = Array.from(this.options).filter(option => option.selected);
            const selectedValues = selectedOptions.map(option => option.value).join(',');

            applyFilter(columnIndex, selectedValues);

            // Highlight the filter symbol for this header
            if (selectedValues === 'all') {
                highlightFilterSymbol(columnIndex, ''); // Remove highlight when 'All' is selected
            } else {
                highlightFilterSymbol(columnIndex, '#ffcc00'); // Change color to your preference
            }

            document.body.removeChild(dropdown);
        };

        const filterSymbol = headers[columnIndex].lastChild;
        const rect = filterSymbol.getBoundingClientRect();
        dropdown.style.position = 'absolute';
        dropdown.style.top = rect.bottom + 'px';
        dropdown.style.left = rect.left + 'px';
        document.body.appendChild(dropdown);
    }



    function applyFilter(columnIndex, filterValue) {
        storedFilters[columnIndex] = filterValue;
        for (let i = 1; i < table.rows.length; i++) {
            let rowMatchesFilters = true;
            for (const index in storedFilters) {
                const cellValue = table.rows[i].cells[index].textContent;
                const filterValues = storedFilters[index].split(',');
                if (storedFilters[index] !== 'all' && !filterValues.includes(cellValue)) {
                    rowMatchesFilters = false;
                    break;
                }
            }
            table.rows[i].style.display = rowMatchesFilters ? '' : 'none';
        }
        sessionStorage.setItem('tableFilters', JSON.stringify(storedFilters));
    }

    function highlightFilterSymbol(columnIndex, color) {
        // Change the color of the filter symbol for the specified header
        const filterSymbol = headers[columnIndex].lastChild;
        filterSymbol.style.color = color;
    }

    
});