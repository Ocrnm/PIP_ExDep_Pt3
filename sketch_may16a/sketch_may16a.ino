int LDR = A0;
int led = 13;
int valorLDR = 0;
int umbralLuz = 1022;

void setup() {
  // put your setup code here, to run once:
   Serial.begin(9600);
   pinMode(led, OUTPUT);
   Serial.println("Sistema iniciado. Umbral por serial:");
}

void loop() {
  if (Serial.available() > 0) {
    String dato = Serial.readStringUntil('\n');
    int nuevoUmbral = dato.toInt();
    if (nuevoUmbral > 0 && nuevoUmbral < 1024) {
      umbralLuz = nuevoUmbral;
      Serial.print("Nuevo umbral: ");
      Serial.println(umbralLuz);
    }
  }

  valorLDR = analogRead(LDR);
  Serial.print("LDR: ");
  Serial.print(valorLDR);
  Serial.print(" | Umbral: ");
  Serial.println(umbralLuz);

  if (valorLDR < umbralLuz) {
    digitalWrite(led, 1);
  } else {
    digitalWrite(led, 0);
  }

  delay(200);
}

