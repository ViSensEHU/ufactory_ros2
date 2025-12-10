// generated from rosidl_typesupport_cpp/resource/idl__type_support.cpp.em
// with input from topic_tools_interfaces:srv/DemuxDelete.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "topic_tools_interfaces/srv/detail/demux_delete__functions.h"
#include "topic_tools_interfaces/srv/detail/demux_delete__struct.hpp"
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

typedef struct _DemuxDelete_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _DemuxDelete_Request_type_support_ids_t;

static const _DemuxDelete_Request_type_support_ids_t _DemuxDelete_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _DemuxDelete_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _DemuxDelete_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _DemuxDelete_Request_type_support_symbol_names_t _DemuxDelete_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, topic_tools_interfaces, srv, DemuxDelete_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, topic_tools_interfaces, srv, DemuxDelete_Request)),
  }
};

typedef struct _DemuxDelete_Request_type_support_data_t
{
  void * data[2];
} _DemuxDelete_Request_type_support_data_t;

static _DemuxDelete_Request_type_support_data_t _DemuxDelete_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _DemuxDelete_Request_message_typesupport_map = {
  2,
  "topic_tools_interfaces",
  &_DemuxDelete_Request_message_typesupport_ids.typesupport_identifier[0],
  &_DemuxDelete_Request_message_typesupport_symbol_names.symbol_name[0],
  &_DemuxDelete_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t DemuxDelete_Request_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_DemuxDelete_Request_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &topic_tools_interfaces__srv__DemuxDelete_Request__get_type_hash,
  &topic_tools_interfaces__srv__DemuxDelete_Request__get_type_description,
  &topic_tools_interfaces__srv__DemuxDelete_Request__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace topic_tools_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<topic_tools_interfaces::srv::DemuxDelete_Request>()
{
  return &::topic_tools_interfaces::srv::rosidl_typesupport_cpp::DemuxDelete_Request_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, topic_tools_interfaces, srv, DemuxDelete_Request)() {
  return get_message_type_support_handle<topic_tools_interfaces::srv::DemuxDelete_Request>();
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
// #include "topic_tools_interfaces/srv/detail/demux_delete__functions.h"
// already included above
// #include "topic_tools_interfaces/srv/detail/demux_delete__struct.hpp"
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

typedef struct _DemuxDelete_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _DemuxDelete_Response_type_support_ids_t;

static const _DemuxDelete_Response_type_support_ids_t _DemuxDelete_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _DemuxDelete_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _DemuxDelete_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _DemuxDelete_Response_type_support_symbol_names_t _DemuxDelete_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, topic_tools_interfaces, srv, DemuxDelete_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, topic_tools_interfaces, srv, DemuxDelete_Response)),
  }
};

typedef struct _DemuxDelete_Response_type_support_data_t
{
  void * data[2];
} _DemuxDelete_Response_type_support_data_t;

static _DemuxDelete_Response_type_support_data_t _DemuxDelete_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _DemuxDelete_Response_message_typesupport_map = {
  2,
  "topic_tools_interfaces",
  &_DemuxDelete_Response_message_typesupport_ids.typesupport_identifier[0],
  &_DemuxDelete_Response_message_typesupport_symbol_names.symbol_name[0],
  &_DemuxDelete_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t DemuxDelete_Response_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_DemuxDelete_Response_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &topic_tools_interfaces__srv__DemuxDelete_Response__get_type_hash,
  &topic_tools_interfaces__srv__DemuxDelete_Response__get_type_description,
  &topic_tools_interfaces__srv__DemuxDelete_Response__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace topic_tools_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<topic_tools_interfaces::srv::DemuxDelete_Response>()
{
  return &::topic_tools_interfaces::srv::rosidl_typesupport_cpp::DemuxDelete_Response_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, topic_tools_interfaces, srv, DemuxDelete_Response)() {
  return get_message_type_support_handle<topic_tools_interfaces::srv::DemuxDelete_Response>();
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
// #include "topic_tools_interfaces/srv/detail/demux_delete__functions.h"
// already included above
// #include "topic_tools_interfaces/srv/detail/demux_delete__struct.hpp"
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

typedef struct _DemuxDelete_Event_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _DemuxDelete_Event_type_support_ids_t;

static const _DemuxDelete_Event_type_support_ids_t _DemuxDelete_Event_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _DemuxDelete_Event_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _DemuxDelete_Event_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _DemuxDelete_Event_type_support_symbol_names_t _DemuxDelete_Event_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, topic_tools_interfaces, srv, DemuxDelete_Event)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, topic_tools_interfaces, srv, DemuxDelete_Event)),
  }
};

typedef struct _DemuxDelete_Event_type_support_data_t
{
  void * data[2];
} _DemuxDelete_Event_type_support_data_t;

static _DemuxDelete_Event_type_support_data_t _DemuxDelete_Event_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _DemuxDelete_Event_message_typesupport_map = {
  2,
  "topic_tools_interfaces",
  &_DemuxDelete_Event_message_typesupport_ids.typesupport_identifier[0],
  &_DemuxDelete_Event_message_typesupport_symbol_names.symbol_name[0],
  &_DemuxDelete_Event_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t DemuxDelete_Event_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_DemuxDelete_Event_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &topic_tools_interfaces__srv__DemuxDelete_Event__get_type_hash,
  &topic_tools_interfaces__srv__DemuxDelete_Event__get_type_description,
  &topic_tools_interfaces__srv__DemuxDelete_Event__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace topic_tools_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<topic_tools_interfaces::srv::DemuxDelete_Event>()
{
  return &::topic_tools_interfaces::srv::rosidl_typesupport_cpp::DemuxDelete_Event_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, topic_tools_interfaces, srv, DemuxDelete_Event)() {
  return get_message_type_support_handle<topic_tools_interfaces::srv::DemuxDelete_Event>();
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
// #include "topic_tools_interfaces/srv/detail/demux_delete__struct.hpp"
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

typedef struct _DemuxDelete_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _DemuxDelete_type_support_ids_t;

static const _DemuxDelete_type_support_ids_t _DemuxDelete_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _DemuxDelete_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _DemuxDelete_type_support_symbol_names_t;
#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _DemuxDelete_type_support_symbol_names_t _DemuxDelete_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, topic_tools_interfaces, srv, DemuxDelete)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, topic_tools_interfaces, srv, DemuxDelete)),
  }
};

typedef struct _DemuxDelete_type_support_data_t
{
  void * data[2];
} _DemuxDelete_type_support_data_t;

static _DemuxDelete_type_support_data_t _DemuxDelete_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _DemuxDelete_service_typesupport_map = {
  2,
  "topic_tools_interfaces",
  &_DemuxDelete_service_typesupport_ids.typesupport_identifier[0],
  &_DemuxDelete_service_typesupport_symbol_names.symbol_name[0],
  &_DemuxDelete_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t DemuxDelete_service_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_DemuxDelete_service_typesupport_map),
  ::rosidl_typesupport_cpp::get_service_typesupport_handle_function,
  ::rosidl_typesupport_cpp::get_message_type_support_handle<topic_tools_interfaces::srv::DemuxDelete_Request>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<topic_tools_interfaces::srv::DemuxDelete_Response>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<topic_tools_interfaces::srv::DemuxDelete_Event>(),
  &::rosidl_typesupport_cpp::service_create_event_message<topic_tools_interfaces::srv::DemuxDelete>,
  &::rosidl_typesupport_cpp::service_destroy_event_message<topic_tools_interfaces::srv::DemuxDelete>,
  &topic_tools_interfaces__srv__DemuxDelete__get_type_hash,
  &topic_tools_interfaces__srv__DemuxDelete__get_type_description,
  &topic_tools_interfaces__srv__DemuxDelete__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace topic_tools_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
get_service_type_support_handle<topic_tools_interfaces::srv::DemuxDelete>()
{
  return &::topic_tools_interfaces::srv::rosidl_typesupport_cpp::DemuxDelete_service_type_support_handle;
}

}  // namespace rosidl_typesupport_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_cpp, topic_tools_interfaces, srv, DemuxDelete)() {
  return ::rosidl_typesupport_cpp::get_service_type_support_handle<topic_tools_interfaces::srv::DemuxDelete>();
}

#ifdef __cplusplus
}
#endif
