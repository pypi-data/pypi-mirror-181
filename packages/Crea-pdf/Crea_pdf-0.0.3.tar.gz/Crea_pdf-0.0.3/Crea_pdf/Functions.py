from reportlab.pdfgen import canvas


def crear(nombre_archivo, contenido):
    #Crea un nuevo documento PDF
    c = canvas.Canvas(f"{nombre_archivo}.pdf")
    c.drawString(0, 8.5 * 72, contenido)
    
    return c.save()
