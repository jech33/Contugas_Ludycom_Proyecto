package herencia.ejemplo2;

public class Estudiante extends Persona {
    int numCuenta;

    public Estudiante(String nombre, int numCuenta) {
        super(nombre);
        this.numCuenta = numCuenta;
    }

    void aprobar() {
        System.out.println("Soy "+nombre+" mi numero de cuenta es "+numCuenta+" y aprobé el examen :)");
    }

    void reprobar() {
        System.out.println("Soy "+nombre+" mi numero de cuenta es "+numCuenta+" y reprobé el examen :(");
    }
    
}
