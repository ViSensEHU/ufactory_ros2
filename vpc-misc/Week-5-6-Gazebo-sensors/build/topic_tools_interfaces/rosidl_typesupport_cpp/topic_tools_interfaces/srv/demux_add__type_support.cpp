// generated from rosidl_typesupport_cpp/resource/idl__type_support.cpp.em
// with input from topic_tools_interfaces:srv/DemuxAdd.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "topic_tools_interfaces/srv/detail/demux_add__functions.h"
#include "topic_tools_interfaces/srv/detail/demux_add__struct.hpp"
#include "rosidl_typesupport_cpp/identifier.hpp"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
#include "rosidl_typesupport_cpp/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace topic_tools_interfaces
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _DemuxAdd_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _DemuxAdd_Request_type_support_ids_t;

static const _DemuxAdd_Request_type_support_ids_t _DemuxAdd_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _DemuxAdd_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _DemuxAdd_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _DemuxAdd_Request_type_support_symbol_names_t _DemuxAdd_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, topic_tools_interfaces, srv, DemuxAdd_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, topic_tools_interfaces, srv, DemuxAdd_Request)),
  }
};

typedef struct _DemuxAdd_Request_type_support_data_t
{
  void * data[2];
} _DemuxAdd_Request_type_support_data_t;

static _DemuxAdd_Request_type_support_data_t _DemuxAdd_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _DemuxAdd_Request_message_typesupport_map = {
  2,
  "topic_tools_interfaces",
  &_DemuxAdd_Request_message_typesupport_ids.typesupport_identifier[0],
  &_DemuxAdd_Request_message_typesupport_symbol_names.symbol_name[0],
  &_DemuxAdd_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t DemuxAdd_Request_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_DemuxAdd_Request_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &topic_tools_interfaces__srv__DemuxAdd_Request__get_type_hash,
  &topic_tools_interfaces__srv__DemuxAdd_Request__get_type_description,
  &topic_tools_interfaces__srv__DemuxAdd_Request__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace topic_tools_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<topic_tools_interfaces::srv::DemuxAdd_Request>()
{
  return &::topic_tools_interfaces::srv::rosidl_typesupport_cpp::DemuxAdd_Request_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, topic_tools_interfaces, srv, DemuxAdd_Request)() {
  return get_message_type_support_handle<topic_tools_interfaces::srv::DemuxAdd_Request>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "topic_tools_interfaces/srv/detail/demux_add__functions.h"
// already included above
// #include "topic_tools_interfaces/srv/detail/demux_add__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace topic_tools_interfaces
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _DemuxAdd_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _DemuxAdd_Response_type_support_ids_t;

static const _DemuxAdd_Response_type_support_ids_t _DemuxAdd_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _DemuxAdd_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _DemuxAdd_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _DemuxAdd_Response_type_support_symbol_names_t _DemuxAdd_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, topic_tools_interfaces, srv, DemuxAdd_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, topic_tools_interfaces, srv, DemuxAdd_Response)),
  }
};

typedef struct _DemuxAdd_Response_type_support_data_t
{
  void * data[2];
} _DemuxAdd_Response_type_support_data_t;

static _DemuxAdd_Response_type_support_data_t _DemuxAdd_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _DemuxAdd_Response_message_typesupport_map = {
  2,
  "topic_tools_interfaces",
  &_DemuxAdd_Response_message_typesupport_ids.typesupport_identifier[0],
  &_DemuxAdd_Response_message_typesupport_symbol_names.symbol_name[0],
  &_DemuxAdd_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t DemuxAdd_Response_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_DemuxAdd_Response_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &topic_tools_interfaces__srv__DemuxAdd_Response__get_type_hash,
  &topic_tools_interfaces__srv__DemuxAdd_Response__get_type_description,
  &topic_tools_interfaces__srv__DemuxAdd_Response__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace topic_tools_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<topic_tools_interfaces::srv::DemuxAdd_Response>()
{
  return &::topic_tools_interfaces::srv::rosidl_typesupport_cpp::DemuxAdd_Response_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, topic_tools_interfaces, srv, DemuxAdd_Response)() {
  return get_message_type_support_handle<topic_tools_interfaces::srv::DemuxAdd_Response>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "topic_tools_interfaces/srv/detail/demux_add__functions.h"
// already included above
// #include "topic_tools_interfaces/srv/detail/demux_add__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace topic_tools_interfaces
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _DemuxAdd_Event_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _DemuxAdd_Event_type_support_ids_t;

static const _DemuxAdd_Event_type_support_ids_t _DemuxAdd_Event_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _DemuxAdd_Event_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _DemuxAdd_Event_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _DemuxAdd_Event_type_support_symbol_names_t _DemuxAdd_Event_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, topic_tools_interfaces, srv, DemuxAdd_Event)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, topic_tools_interfaces, srv, DemuxAdd_Event)),
  }
};

typedef struct _DemuxAdd_Event_type_support_data_t
{
  void * data[2];
} _DemuxAdd_Event_type_support_data_t;

static _DemuxAdd_Event_type_support_data_t _DemuxAdd_Event_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _DemuxAdd_Event_message_typesupport_map = {
  2,
  "topic_tools_interfaces",
  &_DemuxAdd_Event_message_typesupport_ids.typesupport_identifier[0],
  &_DemuxAdd_Event_message_typesupport_symbol_names.symbol_name[0],
  &_DemuxAdd_Event_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t DemuxAdd_Event_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_DemuxAdd_Event_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &topic_tools_interfaces__srv__DemuxAdd_Event__get_type_hash,
  &topic_tools_interfaces__srv__DemuxAdd_Event__get_type_description,
  &topic_tools_interfaces__srv__DemuxAdd_Event__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace topic_tools_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<topic_tools_interfaces::srv::DemuxAdd_Event>()
{
  return &::topic_tools_interfaces::srv::rosidl_typesupport_cpp::DemuxAdd_Event_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, topic_tools_interfaces, srv, DemuxAdd_Event)() {
  return get_message_type_support_handle<topic_tools_interfaces::srv::DemuxAdd_Event>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
#include "rosidl_runtime_c/service_type_support_struct.h"
#include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "topic_tools_interfaces/srv/detail/demux_add__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/service_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace topic_tools_interfaces
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _DemuxAdd_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _DemuxAdd_type_support_ids_t;

static const _DemuxAdd_type_support_ids_t _DemuxAdd_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _DemuxAdd_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _DemuxAdd_type_support_symbol_names_t;
#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _DemuxAdd_type_support_symbol_names_t _DemuxAdd_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, topic_tools_interfaces, srv, DemuxAdd)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, topic_tools_interfaces, srv, DemuxAdd)),
  }
};

typedef struct _DemuxAdd_type_support_data_t
{
  void * data[2];
} _DemuxAdd_type_support_data_t;

static _DemuxAdd_type_support_data_t _DemuxAdd_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _DemuxAdd_service_typesupport_map = {
  2,
  "topic_tools_interfaces",
  &_DemuxAdd_service_typesupport_ids.typesupport_identifier[0],
  &_DemuxAdd_service_typesupport_symbol_names.symbol_name[0],
  &_DemuxAdd_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t DemuxAdd_service_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_DemuxAdd_service_typesupport_map),
  ::rosidl_typesupport_cpp::get_service_typesupport_handle_function,
  ::rosidl_typesupport_cpp::get_message_type_support_handle<topic_tools_interfaces::srv::DemuxAdd_Request>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<topic_tools_interfaces::srv::DemuxAdd_Response>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<topic_tools_interfaces::srv::DemuxAdd_Event>(),
  &::rosidl_typesupport_cpp::service_create_event_message<topic_tools_interfaces::srv::DemuxAdd>,
  &::rosidl_typesupport_cpp::service_destroy_event_message<topic_tools_interfaces::srv::DemuxAdd>,
  &topic_tools_interfaces__srv__DemuxAdd__get_type_hash,
  &topic_tools_interfaces__srv__DemuxAdd__get_type_description,
  &topic_tools_interfaces__srv__DemuxAdd__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace topic_tools_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
get_service_type_support_handle<topic_tools_interfaces::srv::DemuxAdd>()
{
  return &::topic_tools_interfaces::srv::rosidl_typesupport_cpp::DemuxAdd_service_type_support_handle;
}

}  // namespace rosidl_typesupport_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_cpp, topic_tools_interfaces, srv, DemuxAdd)() {
  return ::rosidl_typesupport_cpp::get_service_type_support_handle<topic_tools_interfaces::srv::DemuxAdd>();
}

#ifdef __cplusplus
}
#endif
