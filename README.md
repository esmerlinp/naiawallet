## Naia Wallet

Naia Wallet es una billetera de autocustodia para Bitcoin, creada en Python con Flet. Permite a los usuarios realizar transacciones de Bitcoin de manera segura y eficiente.

### Características principales

- **Tipos de direcciones compatibles:** Naia Wallet trabaja con direcciones de tipo SegWit (p2wpkh y p2wsh) y p2sh-segwit, lo que permite una mayor eficiencia en las transacciones y una menor tarifa de red.
- **Autocustodia:** La información de las firmas no se guarda en ningún servidor central, sino localmente en una base de datos SQLite en el dispositivo del usuario. Esta base de datos se elimina automáticamente al hacer logout, garantizando la privacidad y seguridad de los usuarios.
- **Recuperación de billeteras:** Naia Wallet permite a los usuarios crear y recuperar billeteras de tipo SegWit y p2sh-segwit, proporcionando flexibilidad y control sobre sus activos digitales.
- **Próximos pasos:** En el futuro, se planea implementar una opción para utilizar Naia Wallet como una billetera de solo lectura, donde las transacciones deben ser firmadas con la clave privada guardada de forma externa. Además, se contempla la posibilidad de conectar Naia Wallet a un nodo de Bitcoin para realizar transacciones directamente desde la red Bitcoin.

### Importante

Es importante que los usuarios guarden de forma segura sus frases semilla, ya que esta es la única forma de recuperar sus fondos en caso de pérdida o cambio de dispositivo.

¡Gracias por usar Naia Wallet! Si tienes alguna pregunta o sugerencia, no dudes en abrir un issue en este repositorio. ¡Estamos aquí para ayudar!
