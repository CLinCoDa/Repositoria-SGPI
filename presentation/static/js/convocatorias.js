// presentation/static/js/convocatorias.js

async function fetchConvocatorias(filters = {}) {
    const params = new URLSearchParams(filters);
    const res = await fetch(`/api/convocatorias/?${params.toString()}`);
    return await res.json();
}

async function renderConvocatorias() {


    const yearFilter = document.getElementById('year-filter').value;
    const typeFilter = document.getElementById('type-filter').value;
    const statusFilter = document.getElementById('status-filter').value;
    const searchFilter = document.getElementById('search-filter').value;

    const convocatorias = await fetchConvocatorias({
        year: yearFilter,
        type: typeFilter,
        status: statusFilter,
        search: searchFilter
    });

    const tbody = document.getElementById('convocatorias-body');
    const countMessage = document.getElementById('count-message');
    const noResultsMessage = document.getElementById('no-results-message');
    tbody.innerHTML = '';

    if (convocatorias.length === 0) {
        noResultsMessage.style.display = 'block';
    } else {
        noResultsMessage.style.display = 'none';
    }

    countMessage.innerHTML = `Mostrando <span id="count">${convocatorias.length}</span> convocatorias`;

    convocatorias.forEach(c => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${c.tipo === 'normal' && c.trimestre ? `${c.anio} ${c.trimestre}` : c.anio}</td>
            <td>${c.fecha_inicio}</td>
            <td>${c.fecha_fin}</td>
            <td>${c.tipo}</td>
            <td>${c.estado}</td>
            <td class="btn-cell text-center"></td>
        `;

        // --- Botón Eliminar ---
        const btnDelete = document.createElement('button');
        btnDelete.className = "btn btn-sm btn-danger ms-4"; // me-1 = margin end pequeño
        btnDelete.innerHTML = `<i class="fas fa-trash"></i>`; // icono de eliminar
        btnDelete.title = "Eliminar";
        btnDelete.addEventListener("click", () => deleteConv(c.id));  // ahora seguro llama a la función

        // --- Botón Eliminar ---
        const btnEdit = document.createElement('button');
        btnEdit.className = "btn btn-sm btn-primary";
        btnEdit.innerHTML = `<i class="fas fa-edit"></i>`; // icono de editar
        btnEdit.title = "Editar";
        btnEdit.addEventListener("click", () => editConv(c.id)); // función que debes crear

        row.querySelector(".btn-cell").appendChild(btnEdit);
        row.querySelector(".btn-cell").appendChild(btnDelete);

        tbody.appendChild(row);
    });
}

document.getElementById('reset-filters').addEventListener('click', () => {
    document.getElementById('year-filter').value = "{{ current_year }}";
    document.getElementById('type-filter').value = "all";
    document.getElementById('status-filter').value = "all";
    document.getElementById('search-filter').value = "";
    renderConvocatorias();
});


async function createConvocatoria() {
    const form = document.getElementById('formCrearConvocatoria');
    if (!form.checkValidity()) {
        form.classList.add('was-validated');
        return;
    }

    const tipo = document.getElementById('tipo_convocatoria').value;
    const anio = parseInt(document.getElementById('anio').value);
    const trimestre = tipo === 'normal' ? document.getElementById('trimestre').value : null;
    const fecha_inicio = document.getElementById('fecha_inicio').value;
    const fecha_fin = document.getElementById('fecha_fin').value;
    const descripcion = document.getElementById('descripcion').value;

    await fetch('/api/convocatorias', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ tipo, anio, descripcion, fecha_inicio, fecha_fin, trimestre })
    });

    // Cerrar modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('crearConvocatoriaModal'));
    modal.hide();
    form.reset();
    renderConvocatorias();
}

async function deleteConv(id) {
    console.log("Botón clickeado con id:", id);
    if (!confirm("¿Eliminar convocatoria?")) return;

    const res = await fetch(`/api/convocatorias/${id}`, {
        method: "DELETE"
    });

    const data = await res.json();

    if (data.ok) {
        alert("Convocatoria eliminada");
        renderConvocatorias();
    } else {
        alert("Error: " + data.msg);
    }
}

// Eventos
document.addEventListener('DOMContentLoaded', function () {
    renderConvocatorias();
    document.getElementById('btnGuardarConvocatoria').addEventListener('click', createConvocatoria);
    document.getElementById('year-filter').addEventListener('change', renderConvocatorias);
    document.getElementById('type-filter').addEventListener('change', renderConvocatorias);
    document.getElementById('status-filter').addEventListener('change', renderConvocatorias);
    document.getElementById('search-filter').addEventListener('input', renderConvocatorias);

    // Mostrar/ocultar trimestre
    document.getElementById('tipo_convocatoria').addEventListener('change', function () {
        const container = document.getElementById('trimestreContainer');
        const trimestreSelect = document.getElementById('trimestre');
        if (this.value === 'normal') {
            container.style.display = 'block';
            trimestreSelect.required = true;
        } else {
            container.style.display = 'none';
            trimestreSelect.required = false;
            trimestreSelect.value = '';
        }
    });
});
