export const es = {
  common: {
    welcome: 'Bienvenido',
    save: 'Guardar',
    cancel: 'Cancelar',
    delete: 'Eliminar',
    edit: 'Editar',
    create: 'Crear',
    search: 'Buscar',
    filter: 'Filtrar',
    loading: 'Cargando...',
    noData: 'No hay datos disponibles',
    error: 'Ocurrió un error',
    success: 'Éxito',
    confirm: 'Confirmar',
    back: 'Atrás',
    next: 'Siguiente',
    previous: 'Anterior',
    close: 'Cerrar',
    greeting: '¡Hola, {name}!',
  },

  login: {
    title: 'Daily Helper',
    subtitle: 'Inicia sesión en tu cuenta',
    username: 'Usuario',
    password: 'Contraseña',
    signIn: 'Iniciar Sesión',
    enterUsername: 'Ingresa tu usuario',
    enterPassword: 'Ingresa tu contraseña',
    adminRequired: 'Se requiere acceso de administrador para la gestión de usuarios',
    loginSuccess: 'Inicio de sesión exitoso',
    loginError: 'Credenciales inválidas',
  },

  dashboard: {
    title: 'Panel de Control',
    welcome: '¡Bienvenido, {name}!',
    overview: 'Resumen',
    quickActions: 'Acciones Rápidas',
    stats: {
      total: 'Total',
      active: 'Activo',
      inactive: 'Inactivo',
    },
  },

  users: {
    management: 'Gestión de Usuarios',
    list: 'Lista de Usuarios',
    allUsers: 'Todos los Usuarios',
    createAdmin: 'Crear Administrador',
    createStaff: 'Crear Personal',
    createNormal: 'Crear Usuario Normal',

    types: {
      admin: 'Administrador',
      staff: 'Personal',
      normal: 'Normal',
    },

    form: {
      username: 'Usuario',
      email: 'Correo Electrónico',
      password: 'Contraseña',
      firstName: 'Nombre',
      lastName: 'Apellido',
      isActive: 'Cuenta Activa',

      enterUsername: 'Ingresa el usuario',
      enterEmail: 'Ingresa el correo electrónico',
      enterPassword: 'Ingresa la contraseña',
      enterFirstName: 'Ingresa el nombre',
      enterLastName: 'Ingresa el apellido',

      create: 'Crear Usuario {type}',
      createSuccess: 'Usuario creado exitosamente',
      createError: 'Error al crear usuario',

      updateSuccess: 'Usuario actualizado exitosamente',
      updateError: 'Error al actualizar usuario',

      deleteSuccess: 'Usuario eliminado exitosamente',
      deleteError: 'Error al eliminar usuario',
    },

    table: {
      username: 'Usuario',
      email: 'Correo Electrónico',
      firstName: 'Nombre',
      lastName: 'Apellido',
      role: 'Rol',
      status: 'Estado',
      actions: 'Acciones',
      createdAt: 'Creado el',
      lastLogin: 'Último Acceso',
      joined: 'Registrado',
    },

    info: {
      adminAccount: 'Cuenta de Administrador',
      adminDescription:
        'Este usuario tendrá acceso completo a todas las funciones, incluida la gestión de usuarios.',
      staffAccount: 'Cuenta de Personal',
      staffDescription:
        'Este usuario tendrá privilegios elevados pero sin capacidades de gestión de usuarios.',
      normalAccount: 'Cuenta de Usuario Normal',
      normalDescription: 'Este usuario tendrá acceso estándar sin capacidades administrativas.',
    },

    actions: {
      edit: 'Editar Usuario',
      delete: 'Eliminar Usuario',
      activate: 'Activar',
      deactivate: 'Desactivar',
      resetPassword: 'Restablecer Contraseña',
      refresh: 'Actualizar',
      cannotEditAdmin: 'No se pueden editar usuarios administradores',
      editUser: 'Editar usuario {username}',
    },

    modal: {
      editTitle: 'Editar Usuario: {username}',
      permissions: 'Permisos',
      adminAccess: 'Acceso de Administrador',
      activeAccount: 'Cuenta Activa',
      adminWarning: '⚠️ Los permisos de usuarios administradores no se pueden modificar',
      cancel: 'Cancelar',
      saveChanges: 'Guardar Cambios',
    },
  },

  validation: {
    required: '{field} es requerido',
    minLength: '{field} debe tener al menos {min} caracteres',
    maxLength: '{field} no debe exceder {max} caracteres',
    email: {
      invalid: 'Debe ser un correo electrónico válido',
      required: 'El correo electrónico es requerido',
    },
    password: {
      required: 'La contraseña es requerida',
      minLength: 'La contraseña debe tener al menos {min} caracteres',
      weak: 'La contraseña es demasiado débil',
    },
    username: {
      required: 'El usuario es requerido',
      minLength: 'El usuario debe tener al menos {min} caracteres',
      invalid: 'El usuario contiene caracteres inválidos',
    },
  },

  nav: {
    home: 'Inicio',
    dashboard: 'Panel',
    users: 'Usuarios',
    settings: 'Configuración',
    logout: 'Cerrar Sesión',
    profile: 'Perfil',
  },
}
