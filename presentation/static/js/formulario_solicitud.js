
// Variables globales
let currentStep = 1;
const totalSteps = 5;
let solicitanteCount = 1;
let inventorCount = 1;

// Inicializar formulario
document.addEventListener('DOMContentLoaded', function() {
    updateProgressBar();
    updateStepCounter();
    updateNavigationButtons();
    setupEventListeners();
    initializeFormSummary();
});

// Configurar event listeners
function setupEventListeners() {
    // Navegación entre pasos
    document.getElementById('btn-next').addEventListener('click', nextStep);
    document.getElementById('btn-prev').addEventListener('click', prevStep);
    
    // Agregar solicitantes e inventores
    document.getElementById('btn-agregar-solicitante').addEventListener('click', addSolicitante);
    document.getElementById('btn-agregar-inventor').addEventListener('click', addInventor);
    
    // Validar antes de avanzar
    document.querySelectorAll('.form-section input, .form-section textarea, .form-section select').forEach(input => {
        input.addEventListener('blur', validateCurrentStep);
    });
    
    // Actualizar resumen cuando cambian los datos
    document.getElementById('tituloPatente').addEventListener('input', updateFormSummary);
    document.getElementById('nombre_1').addEventListener('input', updateFormSummary);
    document.getElementById('nombre_inventor_1').addEventListener('input', updateFormSummary);
}

// Navegación entre pasos
function nextStep() {
    if (validateCurrentStep()) {
        if (currentStep < totalSteps) {
            document.getElementById(`section-${currentStep}`).classList.remove('active');
            document.querySelector(`.step[data-step="${currentStep}"]`).classList.remove('active');
            
            currentStep++;
            
            document.getElementById(`section-${currentStep}`).classList.add('active');
            document.querySelector(`.step[data-step="${currentStep}"]`).classList.add('active');
            
            if (currentStep === totalSteps) {
                updateFormSummary();
            }
            
            updateProgressBar();
            updateStepCounter();
            updateNavigationButtons();
            scrollToTop();
        }
    }
}

function prevStep() {
    if (currentStep > 1) {
        document.getElementById(`section-${currentStep}`).classList.remove('active');
        document.querySelector(`.step[data-step="${currentStep}"]`).classList.remove('active');
        
        currentStep--;
        
        document.getElementById(`section-${currentStep}`).classList.add('active');
        document.querySelector(`.step[data-step="${currentStep}"]`).classList.add('active');
        
        updateProgressBar();
        updateStepCounter();
        updateNavigationButtons();
        scrollToTop();
    }
}

// Validar paso actual
function validateCurrentStep() {
    const currentSection = document.getElementById(`section-${currentStep}`);
    const requiredInputs = currentSection.querySelectorAll('[required]');
    let isValid = true;
    
    requiredInputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
        }
    });
    
    // Validación específica para el paso 1 (tipo de patente)
    if (currentStep === 1) {
        const tipoPatente = document.querySelector('input[name="tipo_patente"]:checked');
        if (!tipoPatente) {
            document.getElementById('patenteInvencion').closest('.form-check').classList.add('is-invalid');
            isValid = false;
        } else {
            document.getElementById('patenteInvencion').closest('.form-check').classList.remove('is-invalid');
        }
    }
    
    return isValid;
}

// Actualizar barra de progreso
function updateProgressBar() {
    const progressPercentage = ((currentStep - 1) / (totalSteps - 1)) * 100;
    document.getElementById('progress-bar').style.width = `${progressPercentage}%`;
    
    // Marcar pasos anteriores como completados
    document.querySelectorAll('.step').forEach((step, index) => {
        const stepNumber = parseInt(step.getAttribute('data-step'));
        if (stepNumber < currentStep) {
            step.classList.add('completed');
            step.classList.remove('active');
        } else if (stepNumber === currentStep) {
            step.classList.add('active');
            step.classList.remove('completed');
        } else {
            step.classList.remove('active', 'completed');
        }
    });
}

// Actualizar contador de pasos
function updateStepCounter() {
    document.getElementById('step-counter').textContent = `Paso ${currentStep} de ${totalSteps}`;
}

// Actualizar botones de navegación
function updateNavigationButtons() {
    const btnPrev = document.getElementById('btn-prev');
    const btnNext = document.getElementById('btn-next');
    const btnSubmit = document.getElementById('btn-submit');
    
    if (currentStep === 1) {
        btnPrev.disabled = true;
        btnPrev.style.display = 'inline-block';
        btnNext.style.display = 'inline-block';
        btnSubmit.style.display = 'none';
    } else if (currentStep === totalSteps) {
        btnPrev.disabled = false;
        btnPrev.style.display = 'inline-block';
        btnNext.style.display = 'none';
        btnSubmit.style.display = 'inline-block';
    } else {
        btnPrev.disabled = false;
        btnPrev.style.display = 'inline-block';
        btnNext.style.display = 'inline-block';
        btnSubmit.style.display = 'none';
    }
}

// Agregar solicitante adicional
function addSolicitante() {
    solicitanteCount++;
    const container = document.getElementById('solicitantes-adicionales-container');
    
    const newSolicitante = document.createElement('div');
    newSolicitante.className = 'form-card';
    newSolicitante.innerHTML = `
        <div class="d-flex justify-content-between align-items-center mb-3">
            <h5 class="mb-0">Solicitante ${solicitanteCount}</h5>
            <button type="button" class="btn btn-sm btn-outline-danger btn-remove-solicitante">
                <i class="fas fa-times"></i> Eliminar
            </button>
        </div>
        
        <div class="mb-3">
            <label class="form-label required-field">Tipo de Identificación</label>
            <div class="row">
                <div class="col-auto">
                    <div class="form-check form-check-inline">
                        <input class="form-check-input" type="radio" name="tipo_identificacion_${solicitanteCount}" id="cedula_${solicitanteCount}" value="Cédula">
                        <label class="form-check-label" for="cedula_${solicitanteCount}">Cédula</label>
                    </div>
                </div>
                <div class="col-auto">
                    <div class="form-check form-check-inline">
                        <input class="form-check-input" type="radio" name="tipo_identificacion_${solicitanteCount}" id="ruc_${solicitanteCount}" value="RUC" checked>
                        <label class="form-check-label" for="ruc_${solicitanteCount}">RUC</label>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="row">
            <div class="col-md-6 mb-3">
                <label for="no_identificacion_${solicitanteCount}" class="form-label required-field">No. de Identificación</label>
                <input type="text" class="form-control" id="no_identificacion_${solicitanteCount}" name="no_identificacion_${solicitanteCount}" required>
            </div>
            <div class="col-md-6 mb-3">
                <label for="pais_nacionalidad_${solicitanteCount}" class="form-label required-field">País de Nacionalidad</label>
                <input type="text" class="form-control" id="pais_nacionalidad_${solicitanteCount}" name="pais_nacionalidad_${solicitanteCount}" required>
            </div>
        </div>
        
        <div class="row">
            <div class="col-md-8 mb-3">
                <label for="nombre_${solicitanteCount}" class="form-label required-field">Nombre/Razón Social</label>
                <input type="text" class="form-control" id="nombre_${solicitanteCount}" name="nombre_${solicitanteCount}" required>
            </div>
            <div class="col-md-4 mb-3">
                <label for="provincia_residencia_${solicitanteCount}" class="form-label">Provincia de Residencia</label>
                <input type="text" class="form-control" id="provincia_residencia_${solicitanteCount}" name="provincia_residencia_${solicitanteCount}">
            </div>
        </div>
    `;
    
    container.appendChild(newSolicitante);
    
    // Agregar event listener al botón de eliminar
    newSolicitante.querySelector('.btn-remove-solicitante').addEventListener('click', function() {
        newSolicitante.remove();
        updateFormSummary();
    });
    
    // Actualizar resumen
    updateFormSummary();
}

// Agregar inventor adicional
function addInventor() {
    inventorCount++;
    const container = document.getElementById('inventores-adicionales-container');
    
    const newInventor = document.createElement('div');
    newInventor.className = 'form-card';
    newInventor.innerHTML = `
        <div class="d-flex justify-content-between align-items-center mb-3">
            <h5 class="mb-0">Inventor/Diseñador ${inventorCount}</h5>
            <button type="button" class="btn btn-sm btn-outline-danger btn-remove-inventor">
                <i class="fas fa-times"></i> Eliminar
            </button>
        </div>
        
        <div class="row">
            <div class="col-md-6 mb-3">
                <label for="nombre_inventor_${inventorCount}" class="form-label required-field">Nombre Completo</label>
                <input type="text" class="form-control" id="nombre_inventor_${inventorCount}" name="nombre_inventor_${inventorCount}" required>
            </div>
            <div class="col-md-6 mb-3">
                <label for="email_inventor_${inventorCount}" class="form-label required-field">Email</label>
                <input type="email" class="form-control" id="email_inventor_${inventorCount}" name="email_inventor_${inventorCount}" required>
            </div>
        </div>
    `;
    
    container.appendChild(newInventor);
    
    // Agregar event listener al botón de eliminar
    newInventor.querySelector('.btn-remove-inventor').addEventListener('click', function() {
        newInventor.remove();
        updateFormSummary();
    });
    
    // Actualizar resumen
    updateFormSummary();
}

// Inicializar resumen del formulario
function initializeFormSummary() {
    const summaryContainer = document.getElementById('form-summary');
    summaryContainer.innerHTML = `
        <p class="mb-2"><strong>Título:</strong> <span id="summary-titulo">No especificado</span></p>
        <p class="mb-2"><strong>Tipo de patente:</strong> <span id="summary-tipo">No seleccionado</span></p>
        <p class="mb-2"><strong>Solicitante principal:</strong> <span id="summary-solicitante">No especificado</span></p>
        <p class="mb-2"><strong>Inventores:</strong> <span id="summary-inventores">No especificados</span></p>
        <p class="mb-0"><strong>Documentos a adjuntar:</strong> <span id="summary-documentos">5 documentos obligatorios</span></p>
    `;
}

// Actualizar resumen del formulario
function updateFormSummary() {
    // Título
    const titulo = document.getElementById('tituloPatente').value || 'No especificado';
    document.getElementById('summary-titulo').textContent = titulo;
    
    // Tipo de patente
    const tipoPatente = document.querySelector('input[name="tipo_patente"]:checked');
    document.getElementById('summary-tipo').textContent = tipoPatente ? tipoPatente.value : 'No seleccionado';
    
    // Solicitante principal
    const solicitante = document.getElementById('nombre_1').value || 'No especificado';
    document.getElementById('summary-solicitante').textContent = solicitante;
    
    // Inventores
    const inventores = [];
    for (let i = 1; i <= inventorCount; i++) {
        const inventorInput = document.getElementById(`nombre_inventor_${i}`);
        if (inventorInput && inventorInput.value.trim()) {
            inventores.push(inventorInput.value);
        }
    }
    document.getElementById('summary-inventores').textContent = inventores.length > 0 ? inventores.join(', ') : 'No especificados';
    
    // Conteo de documentos
    const documentosObligatorios = 5;
    const documentosContainer = document.getElementById('summary-documentos');
    documentosContainer.textContent = `${documentosObligatorios} documentos obligatorios`;
}

// Desplazarse al inicio del formulario
function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Manejar envío del formulario
document.getElementById('patentForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Validar todos los pasos
    let formIsValid = true;
    for (let step = 1; step <= totalSteps; step++) {
        // Simular validación de cada paso
        if (step === totalSteps) {
            // Validar la confirmación en el último paso
            const confirmacion = document.getElementById('confirmacion').checked;
            if (!confirmacion) {
                alert('Debe confirmar que la información es verídica antes de enviar.');
                formIsValid = false;
                break;
            }
        }
    }
    
    if (formIsValid) {
        // Mostrar mensaje de éxito
        alert('¡Formulario enviado con éxito! La solicitud de patente ha sido recibida.');
        
        // En un caso real, aquí se enviaría el formulario
        // this.submit();
    }
});

