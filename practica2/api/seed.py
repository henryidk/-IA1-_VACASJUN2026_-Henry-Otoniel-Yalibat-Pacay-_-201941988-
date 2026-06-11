import os
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from database import SessionLocal
from models import Categoria, Pregunta, UsuarioAdmin, Config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def seed():
    db: Session = SessionLocal()
    try:
        _seed_categorias(db)
        _seed_admin(db)
        _seed_config(db)
    except Exception as e:
        db.rollback()
        print(f"Error en seed: {e}")
    finally:
        db.close()


def _seed_admin(db: Session):
    if db.query(UsuarioAdmin).count() > 0:
        return
    admin_user = os.getenv("ADMIN_USER", "IA1-User")
    admin_password = os.getenv("ADMIN_PASSWORD", "IA1-password@_new")
    db.add(UsuarioAdmin(username=admin_user, password=pwd_context.hash(admin_password)))
    db.commit()
    print("Usuario admin creado.")


def _seed_config(db: Session):
    if db.query(Config).filter(Config.clave == "telegram_chat_id").first():
        return
    db.add(Config(clave="telegram_chat_id", valor=""))
    db.commit()


def _seed_categorias(db: Session):
    if db.query(Categoria).count() > 0:
        return

    # --- Categorías ---
    general = Categoria(nombre="Información General", descripcion="Preguntas sobre la institución en general")
    tramites = Categoria(nombre="Trámites y Procedimientos", descripcion="Consultas sobre procesos administrativos")
    horarios = Categoria(nombre="Horarios y Fechas", descripcion="Información sobre calendarios y horarios")

    db.add_all([general, tramites, horarios])
    db.flush()

    # --- Preguntas ---
    preguntas = [
        # Información General
        Pregunta(pregunta="¿Cuál es el horario de atención?", respuesta="Nuestro horario de atención es de lunes a viernes de 8:00 a 17:00 horas.", categoria_id=general.id),
        Pregunta(pregunta="¿Dónde está ubicada la institución?", respuesta="Estamos ubicados en la zona 1 de la ciudad capital, edificio central.", categoria_id=general.id),
        Pregunta(pregunta="¿Cuáles son las carreras disponibles?", respuesta="Ofrecemos las carreras de Ingeniería en Sistemas, Administración de Empresas y Contaduría Pública.", categoria_id=general.id),
        Pregunta(pregunta="¿Cómo puedo contactar a la institución?", respuesta="Puede contactarnos al teléfono 2222-3333 o al correo info@institucion.edu.gt.", categoria_id=general.id),
        Pregunta(pregunta="¿Cuál es el correo electrónico de informes?", respuesta="El correo de informes es informes@institucion.edu.gt.", categoria_id=general.id),
        Pregunta(pregunta="¿Tiene la institución redes sociales?", respuesta="Sí, puede encontrarnos en Facebook, Instagram y Twitter como @InstitucionOficial.", categoria_id=general.id),
        Pregunta(pregunta="¿Qué servicios ofrece la biblioteca?", respuesta="La biblioteca ofrece préstamo de libros, acceso a bases de datos digitales y sala de estudio de lunes a sábado.", categoria_id=general.id),

        # Trámites y Procedimientos
        Pregunta(pregunta="¿Cómo me inscribo a un curso?", respuesta="La inscripción se realiza a través del portal estudiantil en portal.institucion.edu.gt durante el período habilitado.", categoria_id=tramites.id),
        Pregunta(pregunta="¿Qué documentos necesito para inscribirme?", respuesta="Necesita DPI, foto tamaño cédula, título de nivel medio y comprobante de pago de inscripción.", categoria_id=tramites.id),
        Pregunta(pregunta="¿Cómo solicito una constancia de estudios?", respuesta="Puede solicitarla en la ventanilla de Control Académico presentando su carné vigente. El tiempo de entrega es de 3 días hábiles.", categoria_id=tramites.id),
        Pregunta(pregunta="¿Cómo puedo obtener mi título?", respuesta="Debe completar todos los cursos del pensum, aprobar el examen general y cancelar los aranceles correspondientes. Luego solicitar el proceso de graduación.", categoria_id=tramites.id),
        Pregunta(pregunta="¿Cómo solicito una beca?", respuesta="Las solicitudes de beca se presentan en la Dirección de Bienestar Estudiantil durante los primeros 15 días del ciclo.", categoria_id=tramites.id),
        Pregunta(pregunta="¿Dónde realizo el pago de inscripción?", respuesta="Los pagos se realizan en cualquier agencia bancaria con el voucher generado en el portal estudiantil.", categoria_id=tramites.id),
        Pregunta(pregunta="¿Cómo recupero mi contraseña del portal?", respuesta="En la página de inicio del portal haga clic en '¿Olvidaste tu contraseña?' e ingrese su correo institucional.", categoria_id=tramites.id),

        # Horarios y Fechas
        Pregunta(pregunta="¿Cuándo inicia el próximo ciclo académico?", respuesta="El próximo ciclo inicia el 15 de enero. Las inscripciones abren el 1 de diciembre.", categoria_id=horarios.id),
        Pregunta(pregunta="¿Cuándo son los exámenes finales?", respuesta="Los exámenes finales se realizan durante las últimas dos semanas de cada ciclo, según el calendario académico publicado.", categoria_id=horarios.id),
        Pregunta(pregunta="¿Cuándo es el período de inscripciones?", respuesta="El período de inscripciones es del 1 al 31 de diciembre para el ciclo de enero, y del 1 al 30 de mayo para el ciclo de junio.", categoria_id=horarios.id),
        Pregunta(pregunta="¿Cuáles son los días festivos del ciclo?", respuesta="Los días festivos están publicados en el calendario académico disponible en la página oficial de la institución.", categoria_id=horarios.id),
        Pregunta(pregunta="¿Cuándo se publican las notas finales?", respuesta="Las notas finales se publican en el portal estudiantil 5 días hábiles después de finalizado el período de exámenes.", categoria_id=horarios.id),
        Pregunta(pregunta="¿Cuándo es la ceremonia de graduación?", respuesta="La ceremonia de graduación se realiza en junio y diciembre de cada año. Los detalles se informan con anticipación por correo institucional.", categoria_id=horarios.id),
        Pregunta(pregunta="¿Cuál es la fecha límite para retiro de cursos?", respuesta="El retiro de cursos puede realizarse hasta la sexta semana del ciclo sin afectar el índice académico.", categoria_id=horarios.id),
    ]

    db.add_all(preguntas)
    db.commit()
    print("Categorías y preguntas creadas.")


if __name__ == "__main__":
    seed()
