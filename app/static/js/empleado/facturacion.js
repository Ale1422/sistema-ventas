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

    // Agregar accion al boton de busqueda
    document.getElementById('btnBuscar').addEventListener('click', mostrarModalBusqueda)

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

    // Confirmar venta
    // document.getElementById('btnConfirmarVenta').addEventListener('click', function() {
    //     const metodoPago = document.getElementById('metodoPago').value;
        

    //     fetch('/generar_factura', {
    //         method: 'POST',
    //         headers: {
    //             'Content-Type': 'application/json',
    //         },
    //         body: JSON.stringify(data)
    //     })
    //     .then(response => response.json())
    //     .then(data => {
    //         if (data.success) {
    //             alert('Venta registrada con éxito');
    //             window.location.href = `/detalle_factura/${data.factura_id}`;
    //         } else {
    //             alert('Error al registrar la venta: ' + data.error);
    //         }
    //     })
    //     .catch(error => {
    //         console.error('Error:', error);
    //         alert('Error al conectar con el servidor');
    //     });
    // });
});