class GeometricProgression {
    static #count = 0; //приватне статичне поле для підрахунку екземплярів

    #first;  //приватні поля
    #ratio;

    constructor(firstElement, ratio) {
        if (ratio === 0) {
            throw new Error("Знаменник прогресії не може бути нульовим");
        }
        this.#first = firstElement;
        this.#ratio = ratio;
        GeometricProgression.#count++;
        GeometricProgression.#showInfo();
    }

    //приватний статичний метод
    static #showInfo() {
        console.log(`Всього створено ${GeometricProgression.#count} прогресій`);
    }

    //метод для отримання n-го елемента
    getElement(n) {
        return this.#first * (this.#ratio ** (n - 1));
    }

    //метод для отримання перших n елементів
    getFirstNElements(n) {
        const elements = Array.from({length: n}, (_, i) => 
            this.getElement(i + 1).toString());
        return `{${elements.join(", ")}...}`;
    }

    //метод для отримання елементів від k до m
    getElementsFromTo(k, m) {
        if (k > m) return "Неправильний діапазон";
        const elements = Array.from({length: m - k + 1}, (_, i) => 
            this.getElement(i + k).toString());
        return `{${elements.join(", ")}}`;
    }

    //метод для зміни параметрів
    changeParameters(newFirst = null, newRatio = null) {
        if (newFirst !== null) this.#first = newFirst;
        if (newRatio !== null) {
            if (newRatio === 0) throw new Error("Знаменник прогресії не може бути нульовим");
            this.#ratio = newRatio;
        }
    }

    //перевизначення методу toString
    toString() {
        return `& ${this.#first}, ${this.#ratio}: ${this.getFirstNElements(7)}`;
    }

    //метод для порівняння прогресій
    equals(other) {
        if (!(other instanceof GeometricProgression)) return false;
        return this.#first === other.#first && this.#ratio === other.#ratio;
    }
}

//робота класу
try {
    //створюємо екземпляри
    const prog1 = new GeometricProgression(2, 3);
    console.log(prog1.toString());

    const prog2 = new GeometricProgression(1, 2);
    console.log(prog2.toString());

    //отримуємо елементи
    console.log("\nЕлементи від 3 до 5 для prog1:");
    console.log(prog1.getElementsFromTo(3, 5));

    //зміна параметрів
    prog1.changeParameters(null, 2);
    console.log("\nПрогресія 1 після зміни знаменника:");
    console.log(prog1.toString());

    //перевірка рівності
    console.log("\nПеревірка рівності прогресій:");
    console.log("prog1 == prog2:", prog1.equals(prog2));

    //спроба створити прогресію з нульовим знаменником
    const invalidProg = new GeometricProgression(1, 0);
} catch (error) {
    console.log("\nПомилка:", error.message);
}
