// ===================================
// CONFIGURACIÓN Y CONSTANTES
// ===================================
const API_URL = '/api';

// ===================================
// PATRÓN VISITOR PARA EXPORTACIÓN
// ===================================

// Clase base para elementos visitables
class ElementoVisitable {
    accept(visitor) {
        throw new Error('Método accept() debe ser implementado');
    }
}

// Clase Ninja como elemento visitable
class NinjaVisitable extends ElementoVisitable {
    constructor(data) {
        super();
        this.data = data;
    }
    
    accept(visitor) {
        return visitor.visitNinja(this);
    }
}

// Clase Mision como elemento visitable
class MisionVisitable extends ElementoVisitable {
    constructor(data) {
        super();
        this.data = data;
    }
    
    accept(visitor) {
        return visitor.visitMision(this);
    }
}

// Interfaz Visitor
class ExportVisitor {
    visitNinja(ninja) {
        throw new Error('Método visitNinja() debe ser implementado');
    }
    
    visitMision(mision) {
        throw new Error('Método visitMision() debe ser implementado');
    }
    
    getResult() {
        throw new Error('Método getResult() debe ser implementado');
    }
}

// Visitor para exportar a TEXTO
class TextExportVisitor extends ExportVisitor {
    constructor() {
        super();
        this.result = '';
    }
    
    visitNinja(ninja) {
        const n = ninja.data;
        this.result += `========================================\n`;
        this.result += `NINJA: ${n.nombre}\n`;
        this.result += `========================================\n`;
        this.result += `Rango: ${n.rango}\n`;
        this.result += `Aldea: ${n.aldea}\n`;
        this.result += `Estadísticas:\n`;
        this.result += `  - Ataque: ${n.ataque}\n`;
        this.result += `  - Defensa: ${n.defensa}\n`;
        this.result += `  - Chakra: ${n.chakra}\n`;
        this.result += `Jutsus: ${n.jutsus.join(', ') || 'Ninguno'}\n`;
        this.result += `Fecha de Registro: ${new Date(n.fecha_registro).toLocaleDateString()}\n\n`;
    }
    
    visitMision(mision) {
        const m = mision.data;
        this.result += `========================================\n`;
        this.result += `MISIÓN: ${m.nombre}\n`;
        this.result += `========================================\n`;
        this.result += `Rango: ${m.rango}\n`;
        this.result += `Recompensa: ${m.recompensa} Ryō\n`;
        this.result += `Descripción: ${m.descripcion}\n`;
        this.result += `Fecha de Creación: ${new Date(m.fecha_creacion).toLocaleDateString()}\n\n`;
    }
    
    getResult() {
        return this.result;
    }
}

// Visitor para exportar a JSON
class JSONExportVisitor extends ExportVisitor {
    constructor() {
        super();
        this.ninjas = [];
        this.misiones = [];
    }
    
    visitNinja(ninja) {
        this.ninjas.push(ninja.data);
    }
    
    visitMision(mision) {
        this.misiones.push(mision.data);
    }
    
    getResult() {
        return JSON.stringify({
            fecha_exportacion: new Date().toISOString(),
            total_ninjas: this.ninjas.length,
            total_misiones: this.misiones.length,
            ninjas: this.ninjas,
            misiones: this.misiones
        }, null, 2);
    }
}

// Visitor para exportar a XML
class XMLExportVisitor extends ExportVisitor {
    constructor() {
        super();
        this.xml = '<?xml version="1.0" encoding="UTF-8"?>\n';
        this.xml += '<sistema_ninjas>\n';
        this.xml += `  <fecha_exportacion>${new Date().toISOString()}</fecha_exportacion>\n`;
        this.xml += '  <ninjas>\n';
        this.ninjasProcessed = false;
    }
    
    visitNinja(ninja) {
        const n = ninja.data;
        this.xml += '    <ninja>\n';
        this.xml += `      <id>${n.id}</id>\n`;
        this.xml += `      <nombre><![CDATA[${n.nombre}]]></nombre>\n`;
        this.xml += `      <rango>${n.rango}</rango>\n`;
        this.xml += `      <aldea><![CDATA[${n.aldea}]]></aldea>\n`;
        this.xml += `      <estadisticas>\n`;
        this.xml += `        <ataque>${n.ataque}</ataque>\n`;
        this.xml += `        <defensa>${n.defensa}</defensa>\n`;
        this.xml += `        <chakra>${n.chakra}</chakra>\n`;
        this.xml += `      </estadisticas>\n`;
        this.xml += `      <jutsus>\n`;
        n.jutsus.forEach(jutsu => {
            this.xml += `        <jutsu><![CDATA[${jutsu}]]></jutsu>\n`;
        });
        this.xml += `      </jutsus>\n`;
        this.xml += `      <fecha_registro>${n.fecha_registro}</fecha_registro>\n`;
        this.xml += '    </ninja>\n';
    }
    
    visitMision(mision) {
        if (!this.ninjasProcessed) {
            this.xml += '  </ninjas>\n';
            this.xml += '  <misiones>\n';
            this.ninjasProcessed = true;
        }
        
        const m = mision.data;
        this.xml += '    <mision>\n';
        this.xml += `      <id>${m.id}</id>\n`;
        this.xml += `      <nombre><![CDATA[${m.nombre}]]></nombre>\n`;
        this.xml += `      <rango>${m.rango}</rango>\n`;
        this.xml += `      <recompensa>${m.recompensa}</recompensa>\n`;
        this.xml += `      <descripcion><![CDATA[${m.descripcion}]]></descripcion>\n`;
        this.xml += `      <fecha_creacion>${m.fecha_creacion}</fecha_creacion>\n`;
        this.xml += '    </mision>\n';
    }
    
    getResult() {
        if (!this.ninjasProcessed) {
            this.xml += '  </ninjas>\n';
            this.xml += '  <misiones>\n';
        }
        this.xml += '  </misiones>\n';
        this.xml += '</sistema_ninjas>';
        return this.xml;
    }
}

// ===================================
// FUNCIONES DE EXPORTACIÓN
// ===================================

async function exportarDatos(formato) {
    try {
        // Obtener datos de ninjas y misiones
        const [ninjasRes, misionesRes] = await Promise.all([
            fetch(`${API_URL}/ninjas`),
            fetch(`${API_URL}/misiones`)
        ]);
        
        const ninjas = await ninjasRes.json();
        const misiones = await misionesRes.json();
        
        // Crear visitor según el formato
        let visitor;
        let filename;
        let mimeType;
        
        switch(formato) {
            case 'texto':
                visitor = new TextExportVisitor();
                filename = 'reporte_ninjas.txt';
                mimeType = 'text/plain';
                break;
            case 'json':
                visitor = new JSONExportVisitor();
                filename = 'reporte_ninjas.json';
                mimeType = 'application/json';
                break;
            case 'xml':
                visitor = new XMLExportVisitor();
                filename = 'reporte_ninjas.xml';
                mimeType = 'application/xml';
                break;
        }
        
        // Aplicar patrón Visitor
        ninjas.forEach(ninja => {
            const ninjaVisitable = new NinjaVisitable(ninja);
            ninjaVisitable.accept(visitor);
        });
        
        misiones.forEach(mision => {
            const misionVisitable = new MisionVisitable(mision);
            misionVisitable.accept(visitor);
        });
        
        // Obtener resultado
        const resultado = visitor.getResult();
        
        // Mostrar vista previa
        mostrarVistaPrevia(resultado);
        
        // Descargar archivo
        descargarArchivo(resultado, filename, mimeType);
        
        mostrarAlerta('alert-reportes', `Reporte exportado exitosamente en formato ${formato.toUpperCase()}`, 'success');
        
    } catch (error) {
        console.error('Error al exportar:', error);
        mostrarAlerta('alert-reportes', 'Error al exportar datos', 'error');
    }
}

function mostrarVistaPrevia(contenido) {
    const previewArea = document.getElementById('preview-content');
    if (previewArea) {
        previewArea.textContent = contenido;
    }
}

function descargarArchivo(contenido, filename, mimeType) {
    const blob = new Blob([contenido], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
}

// ===================================
// NAVEGACIÓN ENTRE SECCIONES
// ===================================

function showSection(sectionId) {
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.getElementById(sectionId).classList.add('active');
    event.target.classList.add('active');
    
    if (sectionId === 'ninjas') cargarNinjas();
    if (sectionId === 'misiones') cargarMisiones();
    if (sectionId === 'asignaciones') {
        cargarAsignaciones();
        cargarSelectores();
    }
}

// ===================================
// ALERTAS
// ===================================

function mostrarAlerta(containerId, mensaje, tipo) {
    const container = document.getElementById(containerId);
    container.innerHTML = `<div class="alert alert-${tipo}">${mensaje}</div>`;
    setTimeout(() => container.innerHTML = '', 3000);
}

// ===================================
// NINJAS
// ===================================

async function cargarNinjas() {
    try {
        const response = await fetch(`${API_URL}/ninjas`);
        const ninjas = await response.json();
        
        const container = document.getElementById('lista-ninjas');
        container.innerHTML = ninjas.map(ninja => `
            <div class="card">
                <h3>${ninja.nombre}</h3>
                <span class="badge badge-${ninja.rango.toLowerCase()}">${ninja.rango}</span>
                <p><strong>Aldea:</strong> ${ninja.aldea}</p>
                <div class="stats">
                    <div class="stat">⚔️ Ataque: ${ninja.ataque}</div>
                    <div class="stat">🛡️ Defensa: ${ninja.defensa}</div>
                    <div class="stat">💙 Chakra: ${ninja.chakra}</div>
                </div>
                <p><strong>Jutsus:</strong> ${ninja.jutsus.join(', ') || 'Ninguno'}</p>
                <button class="btn-small btn-danger" onclick="eliminarNinja(${ninja.id})">Eliminar</button>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error al cargar ninjas:', error);
    }
}

document.getElementById('form-ninja').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const ninja = {
        nombre: document.getElementById('ninja-nombre').value,
        rango: document.getElementById('ninja-rango').value,
        aldea: document.getElementById('ninja-aldea').value,
        ataque: parseInt(document.getElementById('ninja-ataque').value),
        defensa: parseInt(document.getElementById('ninja-defensa').value),
        chakra: parseInt(document.getElementById('ninja-chakra').value),
        jutsus: document.getElementById('ninja-jutsus').value
    };

    try {
        const response = await fetch(`${API_URL}/ninjas`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(ninja)
        });

        if (response.ok) {
            mostrarAlerta('alert-ninjas', '¡Ninja registrado correctamente!', 'success');
            e.target.reset();
            cargarNinjas();
        } else {
            const error = await response.json();
            mostrarAlerta('alert-ninjas', error.error || 'Error al registrar', 'error');
        }
    } catch (error) {
        mostrarAlerta('alert-ninjas', 'Error de conexión', 'error');
    }
});

async function eliminarNinja(id) {
    if (!confirm('¿Estás seguro de eliminar este ninja?')) return;
    
    try {
        const response = await fetch(`${API_URL}/ninjas/${id}`, { method: 'DELETE' });
        if (response.ok) {
            mostrarAlerta('alert-ninjas', 'Ninja eliminado', 'success');
            cargarNinjas();
        }
    } catch (error) {
        mostrarAlerta('alert-ninjas', 'Error al eliminar', 'error');
    }
}

// ===================================
// MISIONES
// ===================================

async function cargarMisiones() {
    try {
        const response = await fetch(`${API_URL}/misiones`);
        const misiones = await response.json();
        
        const container = document.getElementById('lista-misiones');
        container.innerHTML = misiones.map(mision => `
            <div class="card">
                <h3>${mision.nombre}</h3>
                <span class="badge badge-${mision.rango.toLowerCase()}">Rango ${mision.rango}</span>
                <p><strong>Recompensa:</strong> ${mision.recompensa} Ryō</p>
                <p>${mision.descripcion}</p>
                <button class="btn-small btn-danger" onclick="eliminarMision(${mision.id})">Eliminar</button>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error al cargar misiones:', error);
    }
}

document.getElementById('form-mision').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const mision = {
        nombre: document.getElementById('mision-nombre').value,
        rango: document.getElementById('mision-rango').value,
        recompensa: parseInt(document.getElementById('mision-recompensa').value),
        descripcion: document.getElementById('mision-descripcion').value
    };

    try {
        const response = await fetch(`${API_URL}/misiones`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(mision)
        });

        if (response.ok) {
            mostrarAlerta('alert-misiones', '¡Misión registrada correctamente!', 'success');
            e.target.reset();
            cargarMisiones();
        } else {
            const error = await response.json();
            mostrarAlerta('alert-misiones', error.error || 'Error al registrar', 'error');
        }
    } catch (error) {
        mostrarAlerta('alert-misiones', 'Error de conexión', 'error');
    }
});

async function eliminarMision(id) {
    if (!confirm('¿Estás seguro de eliminar esta misión?')) return;
    
    try {
        const response = await fetch(`${API_URL}/misiones/${id}`, { method: 'DELETE' });
        if (response.ok) {
            mostrarAlerta('alert-misiones', 'Misión eliminada', 'success');
            cargarMisiones();
        }
    } catch (error) {
        mostrarAlerta('alert-misiones', 'Error al eliminar', 'error');
    }
}

// ===================================
// ASIGNACIONES
// ===================================

async function cargarSelectores() {
    try {
        const [ninjasRes, misionesRes] = await Promise.all([
            fetch(`${API_URL}/ninjas`),
            fetch(`${API_URL}/misiones`)
        ]);

        const ninjas = await ninjasRes.json();
        const misiones = await misionesRes.json();

        document.getElementById('asig-ninja').innerHTML = ninjas.map(n => 
            `<option value="${n.id}">${n.nombre} (${n.rango})</option>`
        ).join('');

        document.getElementById('asig-mision').innerHTML = misiones.map(m => 
            `<option value="${m.id}">${m.nombre} (Rango ${m.rango})</option>`
        ).join('');
    } catch (error) {
        console.error('Error al cargar selectores:', error);
    }
}

document.getElementById('form-asignacion').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const asignacion = {
        ninja_id: parseInt(document.getElementById('asig-ninja').value),
        mision_id: parseInt(document.getElementById('asig-mision').value)
    };

    try {
        const response = await fetch(`${API_URL}/asignaciones`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(asignacion)
        });

        if (response.ok) {
            mostrarAlerta('alert-asignaciones', '¡Misión asignada correctamente!', 'success');
            cargarAsignaciones();
        } else {
            const error = await response.json();
            mostrarAlerta('alert-asignaciones', error.error || 'Error al asignar', 'error');
        }
    } catch (error) {
        mostrarAlerta('alert-asignaciones', 'Error de conexión', 'error');
    }
});

async function cargarAsignaciones() {
    try {
        const response = await fetch(`${API_URL}/asignaciones`);
        const asignaciones = await response.json();
        
        const container = document.getElementById('lista-asignaciones');
        container.innerHTML = asignaciones.map(asig => `
            <div class="card">
                <h3>🥷 ${asig.ninja_nombre} ➡️ 📋 ${asig.mision_nombre}</h3>
                <p><strong>Estado:</strong> ${asig.completada ? '✅ Completada' : '⏳ En progreso'}</p>
                <p><strong>Fecha asignación:</strong> ${new Date(asig.fecha_asignacion).toLocaleDateString()}</p>
                ${!asig.completada ? `<button class="btn-small btn-success" onclick="completarMision(${asig.id})">Marcar como Completada</button>` : ''}
            </div>
        `).join('');
    } catch (error) {
        console.error('Error al cargar asignaciones:', error);
    }
}

async function completarMision(id) {
    try {
        const response = await fetch(`${API_URL}/asignaciones/${id}/completar`, {
            method: 'PUT'
        });

        if (response.ok) {
            mostrarAlerta('alert-asignaciones', '¡Misión completada!', 'success');
            cargarAsignaciones();
        }
    } catch (error) {
        mostrarAlerta('alert-asignaciones', 'Error al completar', 'error');
    }
}

// ===================================
// REPORTES
// ===================================

async function cargarReporteNinjas() {
    try {
        const response = await fetch(`${API_URL}/reportes/ninjas`);
        const reporte = await response.json();
        
        const container = document.getElementById('reporte-container');
        container.innerHTML = '<h3>Reporte de Ninjas</h3>' + reporte.map(item => `
            <div class="card">
                <h3>${item.ninja.nombre}</h3>
                <span class="badge badge-${item.ninja.rango.toLowerCase()}">${item.ninja.rango}</span>
                <p><strong>Aldea:</strong> ${item.ninja.aldea}</p>
                <div class="stats">
                    <div class="stat">⚔️ Ataque: ${item.ninja.ataque}</div>
                    <div class="stat">🛡️ Defensa: ${item.ninja.defensa}</div>
                    <div class="stat">💙 Chakra: ${item.ninja.chakra}</div>
                </div>
                <p><strong>Misiones asignadas:</strong> ${item.misiones_asignadas}</p>
                <p><strong>Misiones completadas:</strong> ${item.misiones_completadas}</p>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error al cargar reporte:', error);
    }
}

async function cargarReporteMisiones() {
    try {
        const response = await fetch(`${API_URL}/reportes/misiones`);
        const reporte = await response.json();
        
        const container = document.getElementById('reporte-container');
        container.innerHTML = '<h3>Reporte de Misiones</h3>' + reporte.map(item => `
            <div class="card">
                <h3>${item.mision.nombre}</h3>
                <span class="badge badge-${item.mision.rango.toLowerCase()}">Rango ${item.mision.rango}</span>
                <p><strong>Recompensa:</strong> ${item.mision.recompensa} Ryō</p>
                <p><strong>Ninjas asignados:</strong> ${item.ninjas_asignados.join(', ') || 'Ninguno'}</p>
                <p><strong>Estado:</strong> ${item.completada ? '✅ Completada' : '⏳ Pendiente'}</p>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error al cargar reporte:', error);
    }
}

// ===================================
// INICIALIZACIÓN
// ===================================

// Cargar datos iniciales al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    cargarNinjas();
});