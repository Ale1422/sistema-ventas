function agregarProducto() {
    const codigo = Number(document.getElementById('codigoProducto').value);
    const productoId = codigo > 1000 ? codigo - 1000 : codigo;
    const cantidad = parseFloat(document.getElementById('cantidadProducto').value);

    if(productoId === 0) return alert("Ingresar un codigo");

    // Enviar datos al servidor con fetch
    fetch('/agregar-producto', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ producto_id: productoId, cantidad: cantidad })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }
        actualizarTabla(data);
    })
    .catch(error => console.error('Error:', error));
    limpiarCampos();
    document.getElementById('codigoProducto').focus();
}

function actualizarTabla(data) {
    const tbody = document.getElementById('cuerpoTabla');
    tbody.innerHTML = '';
    total = data.total;

    data.carrito.forEach( producto => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${producto.codigo}</td>
            <td>${producto.nombre}</td>
            <td>${producto.cantidad}</td>
            <td>$${producto.precio_unitario}</td>
            <td>$${producto.subtotal}</td>
            <td>
                <button class="btn btn-sm btn-danger btn-eliminar" onclick="eliminarProducto('${producto.id}')">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });

    document.getElementById('totalFactura').textContent = total.toFixed(2);
    document.getElementById('totalPagar').value = total.toFixed(2);
}

function eliminarProducto(productoId) {
    fetch('/eliminar_producto', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ producto_id: productoId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }

        actualizarTabla(data);
        
    })
    .catch(error => console.error('Error:', error));
}

function limpiarCampos() {
    document.getElementById('codigoProducto').value = '';
    document.getElementById('nombreProducto').value = '';
    document.getElementById('cantidadProducto').value = '1.00';
    document.getElementById('precioProducto').value = '';
}

function mostrarModalBusqueda() {
    $('#buscarProductoModal').modal('show');
    setTimeout(() => {
        let input = document.getElementById('busquedaProducto');
        input.value = '';
        input.focus();
    }, 500);
} 

function buscarProductos() {
    const termino = document.getElementById('busquedaProducto').value;
    fetch(`/buscar_producto?q=${termino}`)
        .then(response => response.json())
        .then(data => {
            const tbody = document.getElementById('resultadosBusqueda');
            tbody.innerHTML = '';
            data.forEach(producto => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${Number(producto.id) + 1000}</td>
                    <td>${producto.nombre}</td>
                    <td>$${producto.precio}</td>
                    <td><button class="btn btn-sm btn-success btn-seleccionar" data-id="${producto.id}">Seleccionar</button></td>
                `;
                tbody.appendChild(tr);
            });

            // Agregar eventos a los botones de selección
            document.querySelectorAll('.btn-seleccionar').forEach(btn => {
                btn.addEventListener('click', function() {
                    const productoId = this.getAttribute('data-id');
                    seleccionarProducto(productoId);
                });
            });
        });
}

function seleccionarProducto(productoId) {
    fetch(`/producto/${productoId}`)
        .then(response => response.json())
        .then(data => {
            if (data) {
                const producto = data;
                document.getElementById('codigoProducto').value = producto.id;
                document.getElementById('nombreProducto').value = producto.nombre;
                document.getElementById('precioProducto').value = producto.precio;
                $('#buscarProductoModal').modal('hide');
                document.getElementById('cantidadProducto').focus();
            }
        });
}

document.addEventListener('DOMContentLoaded', function() {

    const fechaActual = new Date().toLocaleDateString('es-AR');
    document.querySelector('h2').textContent += ` - ${fechaActual}`;

    // Buscar producto por código
    document.getElementById('codigoProducto').addEventListener('input', function() {
        const codigo = this.value;
        if (codigo.length >= 4) {
            console.log("Codigo ", codigo.length);
            fetch(`/buscar_producto?codigo=${codigo}`)
                .then(response => response.json())
                .then(data => {
                    if (data.length > 0) {
                        const producto = data[0];
                        document.getElementById('nombreProducto').value = producto.nombre;
                        document.getElementById('precioProducto').value = producto.precio;
                        document.getElementById('cantidadProducto').focus();
                    }
                });
        }
    });

    // Buscar producto por nombre (modal)
    document.getElementById('btnBuscarProducto').addEventListener('click', buscarProductos);
    document.getElementById('busquedaProducto').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') buscarProductos();
    });

    // Agregar producto al carrito
    document.getElementById('btnAgregar').addEventListener('click', agregarProducto);


    // Botón nueva factura
    document.getElementById('btnNuevaFactura').addEventListener('click', function() {
        if (productos.length > 0 && confirm('¿Está seguro de iniciar una nueva factura? Se perderán los datos actuales.')) {
            productos = [];
            actualizarTabla();
            limpiarCampos();
        }
    });

    // Botón finalizar venta
    document.getElementById('btnFinalizar').addEventListener('click', function() {
        $('#finalizarVentaModal').modal('show');
    });

    const inputNombre = document.getElementById('nombreProducto');
    const listaResultados = document.getElementById('listaResultados');
    
    // Inputs que vamos a rellenar al seleccionar
    const inputPrecio = document.getElementById('precioProducto');
    const inputCodigo = document.getElementById('codigoProducto');

    // let timeoutId; // Para evitar llamar a la API por cada letra rápido (Debounce)

    inputNombre.addEventListener('input', function() {
        const termino = this.value.trim();

        // Ocultar si es muy corto
        if (termino.length <= 3) {
            listaResultados.style.display = 'none';
            return;
        }
        
        buscarProductos(termino);
        
    });

    function buscarProductos(termino) {
        // Llamada a tu ruta Flask
        fetch(`/buscar_producto?q=${encodeURIComponent(termino)}`)
            .then(response => response.json())
            .then(data => {
                mostrarResultados(data);
            })
            .catch(error => console.error('Error:', error));
    }

    function mostrarResultados(productos) {
        // Limpiar lista actual
        listaResultados.innerHTML = '';

        if (productos.length === 0) {
            listaResultados.style.display = 'none';
            return;
        }

        // Crear elementos de la lista
        productos.forEach(producto => {
            // Crear un botón por cada resultado (estilo Bootstrap List Group)
            const item = document.createElement('button');
            item.type = 'button';
            item.classList.add('list-group-item', 'list-group-item-action');
            
            // Contenido del item (Nombre y Precio)
            item.innerHTML = `
                <div class="d-flex justify-content-between align-items-center">
                    <span>${producto.nombre}</span>
                    <span class="badge bg-primary">$${producto.precio}</span>
                </div>
            `;

            // Evento al seleccionar un producto
            item.addEventListener('click', function() {
                seleccionarProducto(producto);
            });

            listaResultados.appendChild(item);
        });

        // Mostrar la lista
        listaResultados.style.display = 'block';
    }

    function seleccionarProducto(producto) {
        // Rellenar los inputs con la info seleccionada
        inputNombre.value = producto.nombre;
        inputPrecio.value = producto.precio; // Asegúrate de que coincida con tu JSON
        inputCodigo.value = producto.id;     // O el campo que uses para código
        
        // Opcional: Enfocar el campo cantidad para agilizar la venta
        document.getElementById('cantidadProducto').focus();

        // Ocultar la lista
        listaResultados.style.display = 'none';
    }

    // Cerrar la lista si se hace clic fuera de ella
    document.addEventListener('click', function(e) {
        if (!inputNombre.contains(e.target) && !listaResultados.contains(e.target)) {
            listaResultados.style.display = 'none';
        }
    });

    const inputCantidad = document.getElementById('cantidadProducto');
    const btnAgregar = document.getElementById('btnAgregar');

    // Función auxiliar para detectar Enter
    function activarBotonConEnter(event) {
        if (event.key === 'Enter') {
            event.preventDefault(); // Evita que se envíe el formulario si está dentro de uno
            btnAgregar.click();     // Simula el clic en el botón Agregar
        }
    }

    // Al dar Enter en la CANTIDAD, se agrega el producto
    inputCantidad.addEventListener('keydown', activarBotonConEnter);
});