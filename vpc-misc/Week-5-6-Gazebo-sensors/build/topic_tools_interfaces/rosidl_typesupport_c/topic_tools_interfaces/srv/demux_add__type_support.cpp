// generated from rosidl_typesupport_c/resource/idl__type_support.cpp.em
// with input from topic_tools_interfaces:srv/DemuxAdd.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "topic_tools_interfaces/srv/detail/demux_add__struct.h"
#include "topic_tools_interfaces/srv/detail/demux_add__type_support.h"
#include "topic_tools_interfaces/srv/detail/demux_add__functions.h"
#include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/message_type_support_dispatch.h"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_c/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace topic_tools_interfaces
{

namespace srv
{

namespace rosidl_typesupport_c
{

typedef struct _DemuxAdd_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _DemuxAdd_Request_type_support_ids_t;

static const _DemuxAdd_Request_type_support_ids_t _DemuxAdd_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
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
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, topic_tools_interfaces, srv, DemuxAdd_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, topic_tools_interfaces, srv, DemuxAdd_Request)),
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
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_DemuxAdd_Request_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &topic_tools_interfaces__srv__DemuxAdd_Request__get_type_hash,
  &topic_tools_interfaces__srv__DemuxAdd_Request__get_type_description,
  &topic_tools_interfaces__srv__DemuxAdd_Request__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace topic_tools_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, topic_tools_interfaces, srv, DemuxAdd_Request)() {
  return &::topic_tools_interfaces::srv::rosidl_typesupport_c::DemuxAdd_Request_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "topic_tools_interfaces/srv/detail/demux_add__struct.h"
// already included above
// #include "topic_tools_interfaces/srv/detail/demux_add__type_support.h"
// already included above
// #include "topic_tools_interfaces/srv/detail/demux_add__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace topic_tools_interfaces
{

namespace srv
{

namespace rosidl_typesupport_c
{

typedef struct _DemuxAdd_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _DemuxAdd_Response_type_support_ids_t;

static const _DemuxAdd_Response_type_support_ids_t _DemuxAdd_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
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
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, topic_tools_interfaces, srv, DemuxAdd_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, topic_tools_interfaces, srv, DemuxAdd_Response)),
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
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_DemuxAdd_Response_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &topic_tools_interfaces__srv__DemuxAdd_Response__get_type_hash,
  &topic_tools_interfaces__srv__DemuxAdd_Response__get_type_description,
  &topic_tools_interfaces__srv__DemuxAdd_Response__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace topic_tools_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, topic_tools_interfaces, srv, DemuxAdd_Response)() {
  return &::topic_tools_interfaces::srv::rosidl_typesupport_c::DemuxAdd_Response_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "topic_tools_interfaces/srv/detail/demux_add__struct.h"
// already included above
// #include "topic_tools_interfaces/srv/detail/demux_add__type_support.h"
// already included above
// #include "topic_tools_interfaces/srv/detail/demux_add__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace topic_tools_interfaces
{

namespace srv
{

namespace rosidl_typesupport_c
{

typedef struct _DemuxAdd_Event_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _DemuxAdd_Event_type_support_ids_t;

static const _DemuxAdd_Event_type_support_ids_t _DemuxAdd_Event_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
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
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, topic_tools_interfaces, srv, DemuxAdd_Event)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, topic_tools_interfaces, srv, DemuxAdd_Event)),
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
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_DemuxAdd_Event_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &topic_tools_interfaces__srv__DemuxAdd_Event__get_type_hash,
  &topic_tools_interfaces__srv__DemuxAdd_Event__get_type_description,
  &topic_tools_interfaces__srv__DemuxAdd_Event__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace topic_tools_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, topic_tools_interfaces, srv, DemuxAdd_Event)() {
  return &::topic_tools_interfaces::srv::rosidl_typesupport_c::DemuxAdd_Event_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "topic_tools_interfaces/srv/detail/demux_add__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/service_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"
#include "service_msgs/msg/service_event_info.h"
#include "builtin_interfaces/msg/time.h"

namespace topic_tools_interfaces
{

namespace srv
{

namespace rosidl_typesupport_c
{
typedef struct _DemuxAdd_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _DemuxAdd_type_support_ids_t;

static const _DemuxAdd_type_support_ids_t _DemuxAdd_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
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
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, topic_tools_interfaces, srv, DemuxAdd)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, topic_tools_interfaces, srv, DemuxAdd)),
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
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_DemuxAdd_service_typesupport_map),
  rosidl_typesupport_c__get_service_typesupport_handle_function,
  &DemuxAdd_Request_message_type_support_handle,
  &DemuxAdd_Response_message_type_support_handle,
  &DemuxAdd_Event_message_type_support_handle,
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_CREATE_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    topic_tools_interfaces,
    srv,
    DemuxAdd
  ),
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_DESTROY_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    topic_tools_interfaces,
    srv,
    DemuxAdd
  ),
  &topic_tools_interfaces__srv__DemuxAdd__get_type_hash,
  &topic_tools_interfaces__srv__DemuxAdd__get_type_description,
  &topic_tools_interfaces__srv__DemuxAdd__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace topic_tools_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_c, topic_tools_interfaces, srv, DemuxAdd)() {
  return &::topic_tools_interfaces::srv::rosidl_typesupport_c::DemuxAdd_service_type_support_handle;
}

#ifdef __cplusplus
}
#endif
