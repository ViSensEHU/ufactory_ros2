// generated from rosidl_typesupport_cpp/resource/idl__type_support.cpp.em
// with input from topic_tools_interfaces:srv/DemuxSelect.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "topic_tools_interfaces/srv/detail/demux_select__functions.h"
#include "topic_tools_interfaces/srv/detail/demux_select__struct.hpp"
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

typedef struct _DemuxSelect_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _DemuxSelect_Request_type_support_ids_t;

static const _DemuxSelect_Request_type_support_ids_t _DemuxSelect_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _DemuxSelect_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _DemuxSelect_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _DemuxSelect_Request_type_support_symbol_names_t _DemuxSelect_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, topic_tools_interfaces, srv, DemuxSelect_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, topic_tools_interfaces, srv, DemuxSelect_Request)),
  }
};

typedef struct _DemuxSelect_Request_type_support_data_t
{
  void * data[2];
} _DemuxSelect_Request_type_support_data_t;

static _DemuxSelect_Request_type_support_data_t _DemuxSelect_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _DemuxSelect_Request_message_typesupport_map = {
  2,
  "topic_tools_interfaces",
  &_DemuxSelect_Request_message_typesupport_ids.typesupport_identifier[0],
  &_DemuxSelect_Request_message_typesupport_symbol_names.symbol_name[0],
  &_DemuxSelect_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t DemuxSelect_Request_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_DemuxSelect_Request_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &topic_tools_interfaces__srv__DemuxSelect_Request__get_type_hash,
  &topic_tools_interfaces__srv__DemuxSelect_Request__get_type_description,
  &topic_tools_interfaces__srv__DemuxSelect_Request__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace topic_tools_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<topic_tools_interfaces::srv::DemuxSelect_Request>()
{
  return &::topic_tools_interfaces::srv::rosidl_typesupport_cpp::DemuxSelect_Request_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, topic_tools_interfaces, srv, DemuxSelect_Request)() {
  return get_message_type_support_handle<topic_tools_interfaces::srv::DemuxSelect_Request>();
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
// #include "topic_tools_interfaces/srv/detail/demux_select__functions.h"
// already included above
// #include "topic_tools_interfaces/srv/detail/demux_select__struct.hpp"
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

typedef struct _DemuxSelect_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _DemuxSelect_Response_type_support_ids_t;

static const _DemuxSelect_Response_type_support_ids_t _DemuxSelect_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _DemuxSelect_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _DemuxSelect_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _DemuxSelect_Response_type_support_symbol_names_t _DemuxSelect_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, topic_tools_interfaces, srv, DemuxSelect_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, topic_tools_interfaces, srv, DemuxSelect_Response)),
  }
};

typedef struct _DemuxSelect_Response_type_support_data_t
{
  void * data[2];
} _DemuxSelect_Response_type_support_data_t;

static _DemuxSelect_Response_type_support_data_t _DemuxSelect_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _DemuxSelect_Response_message_typesupport_map = {
  2,
  "topic_tools_interfaces",
  &_DemuxSelect_Response_message_typesupport_ids.typesupport_identifier[0],
  &_DemuxSelect_Response_message_typesupport_symbol_names.symbol_name[0],
  &_DemuxSelect_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t DemuxSelect_Response_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_DemuxSelect_Response_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &topic_tools_interfaces__srv__DemuxSelect_Response__get_type_hash,
  &topic_tools_interfaces__srv__DemuxSelect_Response__get_type_description,
  &topic_tools_interfaces__srv__DemuxSelect_Response__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace topic_tools_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<topic_tools_interfaces::srv::DemuxSelect_Response>()
{
  return &::topic_tools_interfaces::srv::rosidl_typesupport_cpp::DemuxSelect_Response_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, topic_tools_interfaces, srv, DemuxSelect_Response)() {
  return get_message_type_support_handle<topic_tools_interfaces::srv::DemuxSelect_Response>();
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
// #include "topic_tools_interfaces/srv/detail/demux_select__functions.h"
// already included above
// #include "topic_tools_interfaces/srv/detail/demux_select__struct.hpp"
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

typedef struct _DemuxSelect_Event_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _DemuxSelect_Event_type_support_ids_t;

static const _DemuxSelect_Event_type_support_ids_t _DemuxSelect_Event_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _DemuxSelect_Event_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _DemuxSelect_Event_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _DemuxSelect_Event_type_support_symbol_names_t _DemuxSelect_Event_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, topic_tools_interfaces, srv, DemuxSelect_Event)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, topic_tools_interfaces, srv, DemuxSelect_Event)),
  }
};

typedef struct _DemuxSelect_Event_type_support_data_t
{
  void * data[2];
} _DemuxSelect_Event_type_support_data_t;

static _DemuxSelect_Event_type_support_data_t _DemuxSelect_Event_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _DemuxSelect_Event_message_typesupport_map = {
  2,
  "topic_tools_interfaces",
  &_DemuxSelect_Event_message_typesupport_ids.typesupport_identifier[0],
  &_DemuxSelect_Event_message_typesupport_symbol_names.symbol_name[0],
  &_DemuxSelect_Event_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t DemuxSelect_Event_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_DemuxSelect_Event_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &topic_tools_interfaces__srv__DemuxSelect_Event__get_type_hash,
  &topic_tools_interfaces__srv__DemuxSelect_Event__get_type_description,
  &topic_tools_interfaces__srv__DemuxSelect_Event__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace topic_tools_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<topic_tools_interfaces::srv::DemuxSelect_Event>()
{
  return &::topic_tools_interfaces::srv::rosidl_typesupport_cpp::DemuxSelect_Event_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, topic_tools_interfaces, srv, DemuxSelect_Event)() {
  return get_message_type_support_handle<topic_tools_interfaces::srv::DemuxSelect_Event>();
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
// #include "topic_tools_interfaces/srv/detail/demux_select__struct.hpp"
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

typedef struct _DemuxSelect_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _DemuxSelect_type_support_ids_t;

static const _DemuxSelect_type_support_ids_t _DemuxSelect_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _DemuxSelect_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _DemuxSelect_type_support_symbol_names_t;
#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _DemuxSelect_type_support_symbol_names_t _DemuxSelect_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, topic_tools_interfaces, srv, DemuxSelect)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, topic_tools_interfaces, srv, DemuxSelect)),
  }
};

typedef struct _DemuxSelect_type_support_data_t
{
  void * data[2];
} _DemuxSelect_type_support_data_t;

static _DemuxSelect_type_support_data_t _DemuxSelect_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _DemuxSelect_service_typesupport_map = {
  2,
  "topic_tools_interfaces",
  &_DemuxSelect_service_typesupport_ids.typesupport_identifier[0],
  &_DemuxSelect_service_typesupport_symbol_names.symbol_name[0],
  &_DemuxSelect_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t DemuxSelect_service_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_DemuxSelect_service_typesupport_map),
  ::rosidl_typesupport_cpp::get_service_typesupport_handle_function,
  ::rosidl_typesupport_cpp::get_message_type_support_handle<topic_tools_interfaces::srv::DemuxSelect_Request>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<topic_tools_interfaces::srv::DemuxSelect_Response>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<topic_tools_interfaces::srv::DemuxSelect_Event>(),
  &::rosidl_typesupport_cpp::service_create_event_message<topic_tools_interfaces::srv::DemuxSelect>,
  &::rosidl_typesupport_cpp::service_destroy_event_message<topic_tools_interfaces::srv::DemuxSelect>,
  &topic_tools_interfaces__srv__DemuxSelect__get_type_hash,
  &topic_tools_interfaces__srv__DemuxSelect__get_type_description,
  &topic_tools_interfaces__srv__DemuxSelect__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace topic_tools_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
get_service_type_support_handle<topic_tools_interfaces::srv::DemuxSelect>()
{
  return &::topic_tools_interfaces::srv::rosidl_typesupport_cpp::DemuxSelect_service_type_support_handle;
}

}  // namespace rosidl_typesupport_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_cpp, topic_tools_interfaces, srv, DemuxSelect)() {
  return ::rosidl_typesupport_cpp::get_service_type_support_handle<topic_tools_interfaces::srv::DemuxSelect>();
}

#ifdef __cplusplus
}
#endif
