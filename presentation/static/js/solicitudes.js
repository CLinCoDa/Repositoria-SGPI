// presentation/static/js/solicitudes.js


function viewSolicitud(id) {
    console.log(`Ver solicitud ID: ${id}. Redirigiendo a /solicitudes/${id}`);
    // Implementar redirección o modal
}

function editSolicitud(id) {
    console.log(`Editar solicitud ID: ${id}. Redirigiendo a /solicitudes/editar/${id}`);
    // Implementar redirección o modal
}

async function fetchSolicitudes(filters = {}) {
    const params = new URLSearchParams(filters);
    const res = await fetch(`/api/solicitudes/?${params.toString()}`);

    if (!res.ok) {
        throw new Error(`Error al cargar solicitudes: ${res.statusText}`);
    }

    return await res.json();
}

async function renderSolicitudes() {
    try {
        const estadoFilter = document.getElementById('estado-filter').value;
        const convocatoriaFilter = document.getElementById('convocatoria-filter').value;
        const tipoPIFilter = document.getElementById('tipoPI-filter').value;
        const searchFilter = document.getElementById('search-filter').value;
        
        const solicitudes = await fetchSolicitudes({
            estado: estadoFilter,
            convocatoria_id: convocatoriaFilter,
            tipo_pi: tipoPIFilter,
            search: searchFilter
        });

        const tbody = document.getElementById('solicitudes-body');
        //const countMessage = document.getElementById('count-message');
        const noResultsMessage = document.getElementById('no-results-message');
        tbody.innerHTML = '';
        
        if (solicitudes.length === 0) {
            noResultsMessage.style.display = 'block';
        } else {
            noResultsMessage.style.display = 'none';
        }

        const estadoMap = {
            'borrador': { class: 'bg-warning', text: 'Borrador' },
            'enviada': { class: 'bg-info', text: 'Enviada' },
            'observada': { class: 'bg-danger', text: 'Observada' },
            'validada': { class: 'bg-success', text: 'Validada' },
            'denegada': { class: 'bg-secondary', text: 'Denegada' }
        };

        //countMessage.innerHTML = `Mostrando <span id="count">${convocatorias.length}</span> convocatorias`;

        solicitudes.forEach(s=> {
            // --- 1. Crear la Fila (TR) ---
            const row = document.createElement('tr');

            const estadoInfo = estadoMap[s.estado] || { class: 'bg-secondary', text: s.estado };
            const tipoPiTitle = s.tipo_pi.charAt(0).toUpperCase() + s.tipo_pi.slice(1);

            const tituloTruncado = s.titulo.length > 50 ? s.titulo.substring(0, 50) + '...' : s.titulo;
            const descripcionTruncada = s.descripcion && s.descripcion.length > 80 ? s.descripcion.substring(0, 80) + '...' : s.descripcion;
            
            let fechaEnvioTexto = '<span class="text-muted">No enviada</span>';
            if (s.fecha_envio) {
                // Asume que s.fecha_envio es un string ISO
                const fecha = new Date(s.fecha_envio);
                fechaEnvioTexto = fecha.toLocaleDateString('es-ES', { day: '2-digit', month: '2-digit', year: 'numeric' });
            }


            row.innerHTML = `
                <td><span class="badge bg-light text-dark">${s.codigo}</span></td>
                <td>${s.convocatoria_nombre || 'N/A'}</td>
                <td><span class="badge bg-info">${tipoPiTitle}</span></td>
                <td>
                    <strong>${tituloTruncado}</strong>
                    ${s.descripcion ? `<br><small class="text-muted">${descripcionTruncada}</small>` : ''}
                </td>
                <td>${fechaEnvioTexto}</td>
                <td><span class="badge ${estadoInfo.class}">${estadoInfo.text}</span></td>
                <td class="btn-cell text-center"></td>
            `;

            // --- Creación de Botones (Usando la forma createElement que preferías) ---
            const btnCell = row.querySelector(".btn-cell");
            
            // Botón VER (siempre visible)
            const btnView = document.createElement('a');
            btnView.className = "btn btn-sm btn-outline-primary";
            btnView.innerHTML = `<i class="fas fa-eye"></i>`; 
            btnView.title = "Ver detalles";
            
            btnView.addEventListener("click", () => viewSolicitud(s.id));
            btnCell.appendChild(btnView);

            // Botón EDITAR (si es borrador u observada)
            if (['borrador', 'observada'].includes(s.estado)) {
                const btnEdit = document.createElement('button');
                btnEdit.className = "btn btn-sm btn-outline-warning ms-1";
                btnEdit.innerHTML = `<i class="fas fa-edit"></i>`; 
                btnEdit.title = "Editar";
                btnEdit.addEventListener("click", () => editSolicitud(s.id));
                btnCell.appendChild(btnEdit);
            }
            
            // Botón ELIMINAR (solo si es borrador)
            if (s.estado === 'borrador') {
                const btnDelete = document.createElement('button');
                btnDelete.className = "btn btn-sm btn-outline-danger ms-1";
                btnDelete.innerHTML = `<i class="fas fa-trash"></i>`; 
                btnDelete.title = "Eliminar";
                btnDelete.addEventListener("click", () => deleteSolicitud(s.id));
                btnCell.appendChild(btnDelete);
            }

            tbody.appendChild(row);
        });
    } catch (error) {
        console.error("Error al renderizar solicitudes:", error);
        alert("Ocurrió un error al cargar los datos de las solicitudes.");
    }

    
}

document.getElementById('reset-filters').addEventListener('click', () => {
    document.getElementById('estado-filter').value = "";
    document.getElementById('convocatoria-filter').value = "";
    document.getElementById('tipoPI-filter').value = "";
    document.getElementById('search-filter').value = "";
    renderSolicitudes();
});


async function createSolicitud() {
    
}

async function deleteSolicitud(id) {
    console.log("Botón clickeado con id:", id);
    if (!confirm("¿Eliminar solicitud?")) return;

    const res = await fetch(`/api/solicitudes/${id}`, {
        method: "DELETE"
    });

    const data = await res.json();

    if (data.ok) {
        alert("Solicitud eliminada");
        renderSolicitudes();
    } else {
        alert("Error: " + data.msg);
    }
}

// Eventos
document.addEventListener('DOMContentLoaded', function () {
    renderSolicitudes();
    
    // ... (btnGuardarSolicitud, si existe) ...

    // Escuchadores de Filtros tipo SELECT (evento 'change')
    document.getElementById('estado-filter').addEventListener('change', renderSolicitudes);
    document.getElementById('convocatoria-filter').addEventListener('change', renderSolicitudes);
    document.getElementById('tipoPI-filter').addEventListener('change', renderSolicitudes);
    
    // Escuchador para la búsqueda:
    // 1. Ejecuta la búsqueda al teclear (evento 'input')
    document.getElementById('search-filter').addEventListener('input', renderSolicitudes);
    
    // 2. Ejecuta la búsqueda al hacer clic en el botón (evento 'click')
    const btnSearch = document.getElementById('btnSearch');
    if (btnSearch) {
        btnSearch.addEventListener('click', renderSolicitudes);
    }
});
