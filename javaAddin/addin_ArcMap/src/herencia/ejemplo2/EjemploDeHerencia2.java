package herencia.ejemplo2;

public class EjemploDeHerencia2 {
    public static void main(String[] args) {
        // Crear un estudiante
        Estudiante e = new Estudiante("Alex", 408040);
        e.aprobar();

        Empleado emp=new Empleado("Juan", 5000);
        emp.cobrar();

        e.dormir();
        emp.dormir();
    }
}
