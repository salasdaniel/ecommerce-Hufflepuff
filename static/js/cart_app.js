
let     valor=0;
let     carrito = [];
let     producto = "";
let     precio = 0;
let     last = 1;

const saveLocal = (carrito) =>{
    localStorage.setItem("compra", JSON.stringify(carrito))
}


contenedor.addEventListener('click', (e)=>{

    console.log(e.target.id)

    if ( e.target.nodeName == "INPUT"){
        cadena = (e.target.id)
        
        if (!cadena.includes(last)){
            valor= 0;
        }
        
        last = cadena[cadena.length-1]
        img = ("img"+last)
        imgURL = document.getElementById(img).src
        nombre = ("producto"+last)
        nombre2 = document.getElementById(nombre).textContent.trim() 
        marcador = ("marcador"+last)
        precio = ("precio"+last)
        total = ("total"+last)
        precioUnidad	 = document.getElementById (precio)
        precioNumber = parseInt(precioUnidad.textContent)
    
        if ( e.target.id.includes("aumentar")){

            if (valor >= 0){
            valor++;
            document.getElementById(marcador).textContent = valor
            document.getElementById(total).textContent = precioNumber * valor
            }
            
        } else if ( e.target.id.includes("disminuir")){
            if (valor>0){
                valor --;
                document.getElementById(marcador).textContent = valor
                document.getElementById(total).textContent = precioNumber * valor
            } 
        
        }else if (e.target.id.includes(last)){

            let compra ={
            nombre: nombre2,
            cantidad: document.getElementById(marcador).textContent,
            precio: precioNumber,
            total : document.getElementById(total).textContent,
            imagen : imgURL
            }

            valor = 0;
            document.getElementById(marcador).textContent = valor
            document.getElementById(total).textContent = valor

            carrito.push(compra)
            saveLocal(carrito)
            console.log(carrito)
            
        }

    }

})