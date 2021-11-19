package herencia.ejemplo2;

public class Empleado extends Persona {
    float sueldo;

    public Empleado(String nombre, float sueldo) {
        super(nombre);
        this.sueldo = sueldo;
    }

    void trabajar(){
        System.out.println("Soy "+nombre+" y estoy trabajando");
    }

    void cobrar(){
        System.out.println("Soy "+nombre+" y estoy cobrando y me dieron "+sueldo);
    }
}
