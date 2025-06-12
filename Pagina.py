import pandas as pd
import streamlit as st
import plotly.express as px
from scipy.stats import shapiro, kruskal, f_oneway, pearsonr, chi2_contingency, ks_2samp

# TÍTULO Y CARGA DE ARCHIVO
st.title("SUPERMARKET SALES")
st.write("**REALIZADO POR: Ricardo Cuesta y Juan Altamirano**")
st.write("Sube tu archivo CSV")
file = st.file_uploader("Selecciona el archivo", type=["csv", "xlsx"])

if file is not None:
    #lectura del dataset
    datos = pd.read_csv(file).dropna().drop_duplicates()
    #Introduccion de la pagina
    
    st.write("**Descripcion de la base de Datos**")
    st.write ("Este dataset registra las transacciones individuales de una cadena de supermercados en Myanmar, " \
    "con atributos detallados para cada venta")

   # print(datos.head())
   # print(datos.describe())
    #renombra las columnas para su facil identificacion
    datos = datos.rename (columns={"Branch":"Sucursal","City":"Ciudad","Customer type":"Tipo de Cliente",
                          "Gender":"Género","Product line":"Línea de Producto","Unit price":"Precio unitario","Quantity":"Cantidad",
                          "Tax 5%":"Impuesto 5%","Date":"Fecha de transaccion","Time":"Hora de transaccion","Payment":"Metodo de pago",
                          "cogs":"COGS","gross margin percentage":"Porcentaje margen bruto","gross income":"Ingresos brutos","Rating":"Calificacion"})

    st.write("### Vista previa de los datos")
    st.dataframe(datos.head())

    #Explicacion de las columnas
    st.markdown("### Explicación de las columnas del dataset:")

    st.markdown("""
    **ID de factura:**  
      Identificador único para cada transacción.

    **Sucursal:**  
      La ubicación de la sucursal del supermercado (por ejemplo, Yangon, Naypyitaw, Mandalay).

    **Ciudad:**  
      La ciudad en la que se encuentra ubicada la sucursal del supermercado.

    **Tipo de cliente:**  
      Indica si el cliente es un “Miembro” o “Normal”.

    **Género:**  
      Género del cliente.

    **Línea de producto:**  
      La categoría del producto vendido (por ejemplo, Salud y belleza, Accesorios electrónicos, Hogar y estilo de vida).

    **Precio Unitario:**  
      Precio por unidad del producto.

    **Cantidad:**  
      Número de artículos comprados.

    **Impuesto 5%:**  
      Monto de impuesto calculado sobre la transacción a una tasa del 5%.

    **Total:**  
      Importe total de la transacción, incluidos impuestos.

    **Fecha:**  
    Fecha de la transacción.

    **Hora:**  
      Hora de la transacción.

    **Método de pago**  
      Método de pago utilizado (por ejemplo, efectivo, billetera electrónica, tarjeta de crédito).

    **COGS (Costo de los bienes vendidos):**  
      Representa el costo bruto de los productos.

    **Porcentaje de margen bruto:**  
      Porcentaje fijo de beneficio por cada venta (4,7619%).

    **Ingresos Brutos:**  
      Utilidad obtenida de la transacción.

    **Calificación:**  
      Calificación de satisfacción del cliente (sobre 10).
    """)
    #PARA REALIZAR UN ANALISIS DE CORRELACION MEDIANTE GRAFICAS SE FILTRO EL DATASET
    columnas_seleccionadas = ["COGS","Ingresos brutos","Calificacion","Cantidad"]
    CASO1 = datos[columnas_seleccionadas]
    #SELECCIONAMOS COLUMNAS SOLO CON DATOS NUMERICOS
    Corr_num = CASO1.select_dtypes("number")
    fig2 = px.scatter_matrix(
        CASO1,
        title=f"Correlaciones entre variables",
    )
    st.plotly_chart(fig2)
    st.write("A simple vista vamos a examinar la correlacion entre Cantidad VS Total")
    #realizo el primer analisis/////////////////////////////////////////////////////////////////////////////////////////////
    st.write("### ANALISIS 1")
    #grafico de dispersion 
    fig3 = px.scatter(datos, x="Cantidad", y="Total", title="Cantidad vs Total")
    st.plotly_chart(fig3)
    #pestana de visualizacion de la prueba
    prueba1=st.toggle('Realizar prueba de Pearson r')
    if prueba1:
        st.write("### Resultado de la prueba Pearson r")
        r, p = pearsonr(datos["Cantidad"], datos["Total"])
        st.write(f"Coeficiente de Pearson r = {r:.3f}")
        st.write(f"p-value = {p:.5f}")
        st.markdown ("**CONCLUSION**")
        st.write("¿Existe relación entre la cantidad de productos comprados y el ingreso bruto obtenido?")
        st.write("Sí. Se encontró una correlación positiva significativa, lo que indica que a mayor cantidad comprada, mayor es el ingreso bruto. " \
        "Esto tiene sentido ya que el ingreso depende de la cantidad vendida.")
    
    #realizo el segundo analisis///////////////////////////////////////////////////////////
    st.write("### ANALISIS 2")
    #grafico de cajas
    fig4 = px.box(datos, x="Tipo de Cliente", y="Total",color="Tipo de Cliente" ,title="Monto de compras por Tipo de Cliente")
    st.plotly_chart(fig4)
  
  #pestana de visualizacion de la prueba
    prueba2=st.toggle('Realizar prueba de normalidad')
    if prueba2:
        st.write("### Resultado de la prueba")
        tipo1 = datos[datos["Tipo de Cliente"] == "Member"]["Total"]
        tipo2 = datos[datos["Tipo de Cliente"] == "Normal"]["Total"]

        # Prueba de normalidad para elegir test
        p1 = shapiro(tipo1)[1] #accedo al segundo valor
        p2 = shapiro(tipo2)[1] #accedo al segundo valor
        #condicional para escoger la prueba
        if p1 > 0.05 and p2 > 0.05:
            stat, p = f_oneway(tipo1, tipo2)
            st.write("Prueba de ANOVA realizada ya que sigue una distribucion normal")
        else:
            stat, p = kruskal(tipo1, tipo2)
            st.write("Prueba de Kruskal-Wallis realizada ya que no sigue una distribucion normal")

        st.write(f"p-value = {p:.5f}")
        st.markdown ("**CONCLUSION**")
        st.write("¿Existe relación entre la afiliacion del cliente y el monto total de compras?")
        st.write( "Al comparar el monto total de las compras entre clientes clasificados como “Miembro” y “Normal," 
                 " no se encontraron diferencias estadísticamente significativas (p > 0.05). Esto sugiere que el tipo de afiliación del cliente"
                 " no influye de manera relevante en el valor total de sus compras. Por tanto, el comportamiento de compra es similar en ambos segmentos.")
    #realizo el tercer analisis\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    st.write("### ANALISIS 3")
    # Tabla de contingencia
    tabla = pd.crosstab(datos["Tipo de Cliente"], datos["Metodo de pago"])
    # Mostrar tabla en pantalla
    st.write("### Tabla de frecuencias")
    st.dataframe(tabla)

    # Gráfico de barras 
    fig5 = px.bar(tabla, barmode='group', title="Método de pago por tipo de cliente")
    st.plotly_chart(fig5)
    #pestana de visualizacion de la prueba
    prueba3=st.toggle('Realizar prueba de CHI Cuadrado')
    if prueba3:
        # Prueba de Chi-cuadrado
        chi2_stat, p_val, dof, expected = chi2_contingency(tabla)

        # Mostrar resultado
        st.write("### Resultado de la prueba Chi-cuadrado")
        st.write(f"Estadístico chi = {chi2_stat:.3f}")
        st.write(f"p-value = {p_val:.5f}")

        st.markdown ("**CONCLUSION**")
        if p_val < 0.05:
            st.write("Existe una asociación significativa entre tipo de cliente y método de pago.")
        else:
            st.write("No hay una asociación estadísticamente significativa entre tipo de cliente y método de pago.")
        st.write("¿Existe  alguna relación entre la el tipo de cliente y metodo de pago?")
        st.write("Según el análisis de chi-cuadrado aplicado a las variables “tipo de cliente” y “método de pago”," 
                 " no se encontró evidencia estadísticamente significativa de una asociación entre ambas (p ≈ 0.073 > 0.05)." 
                 " Esto sugiere que la elección del método de pago no depende de si el cliente es miembro o no, al menos en este conjunto de datos." 
                 " Aunque existen diferencias visuales leves en el gráfico, estas no son suficientes para confirmar una relación estadística.")

    #realizo el cuarto analisis\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    st.write("### ANALISIS 4")
    #Grafico que nos muestra el genero de los datos que se tiene como muestra 
    genero= datos.groupby("Género").count().reset_index()
    st.write("## Gráfico de pastel sobre el Género de toda la muestra")
    Fig1= px.pie(genero, values="Invoice ID", names= "Género")
    st.plotly_chart(Fig1)
    st.write("Se observa que la muestra de genero es igual para la obtencion de datos")

    st.write("## Género vs Línea de Producto")
    tabla2 = pd.crosstab(datos["Género"], datos["Línea de Producto"])
    st.dataframe(tabla2)

    prueba4=st.toggle('Realizar prueba de CHI Cuadrado ')
    if prueba4:
        # Prueba de Chi-cuadrado
        chi2_stat2, p_val2, dof, expected = chi2_contingency(tabla2)

        # Mostrar resultado
        st.write("### Resultado de la prueba Chi-cuadrado")
        st.write(f"Estadístico chi = {chi2_stat2:.3f}")
        st.write(f"p-value = {p_val2:.5f}")

        st.markdown ("**CONCLUSION**")
        if p_val2 < 0.05:
            st.write("Existe una asociación significativa entre genero y el tipo de linea del producto.")
        else:
            st.write("No hay una asociación estadísticamente significativa entre genero y el tipo de linea del producto.")
        st.write("¿Qué asosciacion existe entre el genero y el tipo de linea de producto?")    
        st.write("El análisis de independencia entre el género del cliente y la línea de producto adquirida no mostró una asociación estadísticamente "
                 "significativa (p > 0.05). " 
                 " Esto indica que, en este conjunto de datos, la distribución de compras por categoría de producto es similar " 
                 " entre hombres y mujeres, sin diferencias relevantes desde el punto de vista estadístico")
  # REALIZO EL ANALISIS 5\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    st.write("### ANALISIS 5")
    st.write("## Calificación según Sucursal")
    fig5 = px.box(datos, x="Sucursal", y="Calificacion", color="Sucursal", title="Calificacion por Sucursal")
    st.plotly_chart(fig5)
    prueba5=st.toggle('Realizar prueba estadistica')
    if prueba5:
        rating_A = datos[datos["Sucursal"] == "A"]["Calificacion"]
        rating_B = datos[datos["Sucursal"] == "B"]["Calificacion"]
        rating_C = datos[datos["Sucursal"] == "C"]["Calificacion"]
        #obtengo la pruebas de normalidad para cada sucursalque me servirar para la condicion siguiente
        pA = shapiro(rating_A)[1]#accedo al segundo valor
        pB = shapiro(rating_B)[1]#accedo al segundo valor
        pC = shapiro(rating_C)[1]#accedo al segundo valor
        
        st.markdown ("**CONCLUSION**")
        if pA > 0.05 and pB > 0.05 and pC > 0.05:
            stat, pval5 = f_oneway(rating_A, rating_B, rating_C)
            st.write("Prueba de ANOVA realizada ya que sigue una distribucion normal")
        else:
            stat, pval5 = kruskal(rating_A, rating_B, rating_C)
            st.write("Prueba de Kruskal-Wallis realizada ya que no sigue una distribucion normal")

        st.write(f"p-value = {pval5:.5f}")
        st.write("¿Qué asosciacion existe entre la sucursal y su calificación?") 
        st.write("Dado que el valor de p es mayor a 0.05, no se encontraron diferencias estadísticamente" 
                " significativas en las calificaciones otorgadas por los clientes entre las sucursales A, B y C."
                " Esto sugiere que la experiencia del cliente, medida por su calificación, es similar en las tres sucursales"
                " analizadas, al menos desde una perspectiva estadística.")