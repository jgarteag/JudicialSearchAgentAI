# Judicial Search Agent AI

Bot de Telegram para buscar radicados judiciales en PDFs usando IA y arquitectura hexagonal.

## 📁 Estructura del proyecto

```
JudicialSearchAgentAI/
├── radicados-bot/              # Código de la aplicación
│   ├── src/
│   │   ├── domain/            # Lógica de negocio
│   │   ├── application/       # Servicios de aplicación
│   │   ├── infrastructure/    # Adaptadores (MongoDB, PDF, Telegram)
│   │   └── main.py           # Entry point
│   ├── requirements.txt
│   └── README.md
│
└── terraform-radicados-bot/    # Infraestructura como código
    ├── ec2/
    │   ├── main.tf
    │   ├── variables.tf
    │   ├── outputs.tf
    │   └── user_data.sh
    └── README.md
```

## 🚀 Despliegue en AWS EC2

### Prerequisitos

- Terraform >= 1.0 instalado
- AWS CLI configurado con perfil `SandboxNQ`
- Código en GitHub (rama main)

### Despliegue inicial

1. **Configurar credenciales**

```bash
cd terraform-radicados-bot/ec2
cp terraform.tfvars.example terraform.tfvars
# Editar terraform.tfvars con tus valores
```

2. **Desplegar infraestructura**

```bash
terraform init
terraform plan
terraform apply
```

Espera 2-3 minutos para que el bot se instale automáticamente.

## 🔄 Actualizar el bot con cambios de código

Cuando hagas cambios en el código y quieras actualizar la instancia EC2:

### Paso 1: Subir cambios a GitHub

```bash
cd radicados-bot/
git add .
git commit -m "Descripción de tus cambios"
git push origin main
```

### Paso 2: Recrear instancia EC2

```bash
cd ../terraform-radicados-bot/ec2/
terraform apply -replace="aws_instance.radicados_bot" -auto-approve
```

⏱️ **Tiempo de actualización**: 2-3 minutos

El bot se actualizará automáticamente con el código nuevo de GitHub.

## 🤖 Uso del bot

1. Busca el bot en Telegram
2. Envía `/start` para iniciar
3. Envía uno o varios PDFs
4. Usa `/buscar` para ver los juzgados disponibles
5. Escribe el número del juzgado
6. Recibe los radicados encontrados

### Comandos disponibles

- `/start` - Iniciar el bot y ver ayuda
- `/buscar` o `/juzgados` - Ver lista de juzgados disponibles
- `/consulta` - Descargar CSV consolidado con todos los radicados de todas las colecciones

## 📊 Monitoreo

### Ver estado de la instancia

```bash
cd terraform-radicados-bot/ec2/
terraform output
```

### Ver logs del bot

```bash
aws ssm start-session \
  --target $(terraform output -raw instance_id) \
  --profile SandboxNQ

# Una vez conectado:
sudo journalctl -u radicados-bot -f
```

## 🗑️ Destruir infraestructura

```bash
cd terraform-radicados-bot/ec2/
terraform destroy
```

**Nota**: La Elastic IP debe eliminarse manualmente desde la consola de AWS.

## 🏗️ Arquitectura

### Aplicación (radicados-bot/)

- **Arquitectura Hexagonal**: Separación clara entre dominio, aplicación e infraestructura
- **Clean Code**: Código limpio y mantenible
- **Domain**: Entidades (Radicado, Juzgado) y casos de uso
- **Application**: Servicios que coordinan la lógica
- **Infrastructure**: Adaptadores para MongoDB, PDF y Telegram

### Infraestructura (terraform-radicados-bot/)

- **EC2 Instance (t3.micro)**: ~$7-9/mes
- **Security Group**: Solo permite salida a internet
- **Elastic IP**: IP pública fija
- **User Data**: Instalación automática del bot

## 🔧 Desarrollo local

### Instalar dependencias

```bash
cd radicados-bot/
pip install -r requirements.txt
```

### Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con tus credenciales
```

### Ejecutar el bot

```bash
python src/main.py
```

## 📝 Notas importantes

- El bot corre 24/7 en AWS EC2
- Se reinicia automáticamente si falla
- Las credenciales están en AWS (no en el código)
- Cada actualización requiere recrear la instancia
- El archivo `terraform.tfvars` NO debe subirse a Git

## 🐛 Troubleshooting

### El bot no responde

1. Verifica que la instancia esté corriendo
2. Espera 2-3 minutos después del deploy
3. Revisa los logs del bot

### Cambios no se reflejan

1. Confirma que hiciste `git push origin main`
2. Usa `-replace` para forzar recreación
3. Espera 2-3 minutos para la instalación

### Error al aplicar Terraform

- Verifica el perfil AWS `SandboxNQ`
- Confirma permisos en AWS
- Revisa que el código esté en GitHub

## 📚 Documentación adicional

- [Documentación del bot](radicados-bot/README.md)
- [Documentación de infraestructura](terraform-radicados-bot/README.md)
