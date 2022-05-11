# Adquisición de datos PulsiOXimetro con representación en gráfica

<p align="center">
<img src="https://user-images.githubusercontent.com/46607004/154055355-a45a597b-4c16-4460-a285-ad0554636bdf.png" alt="drawing" width="200"/>
</p>

Existen dos pogramas:
        - Plot_Continuo:  cada muestra que se coje desde el sensor se muestra en la gráfica
        - Plot_periodico: se recogen datos durante un periodo, y después se muestran en la gráfica
No hay ningún criterio de tiempo real y se produce time-slicing (Se va perdiendo tiempo en las tareas)

En ambos casos, se abriráuna ventana con dos gráficas, en la superior aparecerán los datos correspondientes
a las medidas tomadas por el sensor infrarrojo, y en la inferior, los correspondientes al rojo.