package herencia.ejemplo1;

class Animal {}
class Perro extends Animal {}
class Gato extends Animal {}

public class ejemploHerencia {
    public static void main(String[] args) {
        Animal a = new Animal();
        Perro p = new Perro();
        Gato g = new Gato();

        System.out.println("Comparacion de animales");
        System.out.println("Comparacion de objeto animal: " + (a instanceof Animal));
        System.out.println("Comparacion de objeto perro: " + (p instanceof Animal));
        System.out.println("Comparacion de objeto gato: " + (g instanceof Animal));
        System.out.println("");
        System.out.println("Comparacion de perros");
        System.out.println("Comparacion de objeto animal: " + (a instanceof Perro));
        System.out.println("Comparacion de objeto perro: " + (p instanceof Perro));
    }
}
