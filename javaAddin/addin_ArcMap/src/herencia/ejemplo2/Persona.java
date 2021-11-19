package herencia.ejemplo2;

public class Persona {
    String nombre;

    public Persona(String nombre) {
        this.nombre = nombre;
    }

    void dormir() {
        System.out.println("Soy "+nombre+" y estoy durmiendo");
    }

    void respirar() {
        System.out.println("Soy "+nombre+" y estoy respirando");
    }

    void comer() {
        System.out.println("Soy "+nombre+" y estoy comiendo");
    }
}
