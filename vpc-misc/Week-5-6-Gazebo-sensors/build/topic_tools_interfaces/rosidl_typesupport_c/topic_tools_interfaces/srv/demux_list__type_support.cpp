// generated from rosidl_typesupport_c/resource/idl__type_support.cpp.em
// with input from topic_tools_interfaces:srv/DemuxList.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "topic_tools_interfaces/srv/detail/demux_list__struct.h"
#include "topic_tools_interfaces/srv/detail/demux_list__type_support.h"
#include "topic_tools_interfaces/srv/detail/demux_list__functions.h"
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

typedef struct _DemuxList_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _DemuxList_Request_type_support_ids_t;

static const _DemuxList_Request_type_support_ids_t _DemuxList_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _DemuxList_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _DemuxList_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _DemuxList_Request_type_support_symbol_names_t _DemuxList_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, topic_tools_interfaces, srv, DemuxList_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, topic_tools_interfaces, srv, DemuxList_Request)),
  }
};

typedef struct _DemuxList_Request_type_support_data_t
{
  void * data[2];
} _DemuxList_Request_type_support_data_t;

static _DemuxList_Request_type_support_data_t _DemuxList_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _DemuxList_Request_message_typesupport_map = {
  2,
  "topic_tools_interfaces",
  &_DemuxList_Request_message_typesupport_ids.typesupport_identifier[0],
  &_DemuxList_Request_message_typesupport_symbol_names.symbol_name[0],
  &_DemuxList_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t DemuxList_Request_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_DemuxList_Request_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &topic_tools_interfaces__srv__DemuxList_Request__get_type_hash,
  &topic_tools_interfaces__srv__DemuxList_Request__get_type_description,
  &topic_tools_interfaces__srv__DemuxList_Request__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace topic_tools_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, topic_tools_interfaces, srv, DemuxList_Request)() {
  return &::topic_tools_interfaces::srv::rosidl_typesupport_c::DemuxList_Request_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "topic_tools_interfaces/srv/detail/demux_list__struct.h"
// already included above
// #include "topic_tools_interfaces/srv/detail/demux_list__type_support.h"
// already included above
// #include "topic_tools_interfaces/srv/detail/demux_list__functions.h"
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

typedef struct _DemuxList_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _DemuxList_Response_type_support_ids_t;

static const _DemuxList_Response_type_support_ids_t _DemuxList_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _DemuxList_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _DemuxList_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _DemuxList_Response_type_support_symbol_names_t _DemuxList_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, topic_tools_interfaces, srv, DemuxList_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, topic_tools_interfaces, srv, DemuxList_Response)),
  }
};

typedef struct _DemuxList_Response_type_support_data_t
{
  void * data[2];
} _DemuxList_Response_type_support_data_t;

static _DemuxList_Response_type_support_data_t _DemuxList_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _DemuxList_Response_message_typesupport_map = {
  2,
  "topic_tools_interfaces",
  &_DemuxList_Response_message_typesupport_ids.typesupport_identifier[0],
  &_DemuxList_Response_message_typesupport_symbol_names.symbol_name[0],
  &_DemuxList_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t DemuxList_Response_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_DemuxList_Response_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &topic_tools_interfaces__srv__DemuxList_Response__get_type_hash,
  &topic_tools_interfaces__srv__DemuxList_Response__get_type_description,
  &topic_tools_interfaces__srv__DemuxList_Response__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace topic_tools_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, topic_tools_interfaces, srv, DemuxList_Response)() {
  return &::topic_tools_interfaces::srv::rosidl_typesupport_c::DemuxList_Response_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "topic_tools_interfaces/srv/detail/demux_list__struct.h"
// already included above
// #include "topic_tools_interfaces/srv/detail/demux_list__type_support.h"
// already included above
// #include "topic_tools_interfaces/srv/detail/demux_list__functions.h"
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

typedef struct _DemuxList_Event_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _DemuxList_Event_type_support_ids_t;

static const _DemuxList_Event_type_support_ids_t _DemuxList_Event_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _DemuxList_Event_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _DemuxList_Event_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _DemuxList_Event_type_support_symbol_names_t _DemuxList_Event_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, topic_tools_interfaces, srv, DemuxList_Event)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, topic_tools_interfaces, srv, DemuxList_Event)),
  }
};

typedef struct _DemuxList_Event_type_support_data_t
{
  void * data[2];
} _DemuxList_Event_type_support_data_t;

static _DemuxList_Event_type_support_data_t _DemuxList_Event_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _DemuxList_Event_message_typesupport_map = {
  2,
  "topic_tools_interfaces",
  &_DemuxList_Event_message_typesupport_ids.typesupport_identifier[0],
  &_DemuxList_Event_message_typesupport_symbol_names.symbol_name[0],
  &_DemuxList_Event_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t DemuxList_Event_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_DemuxList_Event_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &topic_tools_interfaces__srv__DemuxList_Event__get_type_hash,
  &topic_tools_interfaces__srv__DemuxList_Event__get_type_description,
  &topic_tools_interfaces__srv__DemuxList_Event__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace topic_tools_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, topic_tools_interfaces, srv, DemuxList_Event)() {
  return &::topic_tools_interfaces::srv::rosidl_typesupport_c::DemuxList_Event_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "topic_tools_interfaces/srv/detail/demux_list__type_support.h"
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
typedef struct _DemuxList_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _DemuxList_type_support_ids_t;

static const _DemuxList_type_support_ids_t _DemuxList_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _DemuxList_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _DemuxList_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _DemuxList_type_support_symbol_names_t _DemuxList_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, topic_tools_interfaces, srv, DemuxList)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, topic_tools_interfaces, srv, DemuxList)),
  }
};

typedef struct _DemuxList_type_support_data_t
{
  void * data[2];
} _DemuxList_type_support_data_t;

static _DemuxList_type_support_data_t _DemuxList_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _DemuxList_service_typesupport_map = {
  2,
  "topic_tools_interfaces",
  &_DemuxList_service_typesupport_ids.typesupport_identifier[0],
  &_DemuxList_service_typesupport_symbol_names.symbol_name[0],
  &_DemuxList_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t DemuxList_service_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_DemuxList_service_typesupport_map),
  rosidl_typesupport_c__get_service_typesupport_handle_function,
  &DemuxList_Request_message_type_support_handle,
  &DemuxList_Response_message_type_support_handle,
  &DemuxList_Event_message_type_support_handle,
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_CREATE_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    topic_tools_interfaces,
    srv,
    DemuxList
  ),
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_DESTROY_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    topic_tools_interfaces,
    srv,
    DemuxList
  ),
  &topic_tools_interfaces__srv__DemuxList__get_type_hash,
  &topic_tools_interfaces__srv__DemuxList__get_type_description,
  &topic_tools_interfaces__srv__DemuxList__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace topic_tools_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_c, topic_tools_interfaces, srv, DemuxList)() {
  return &::topic_tools_interfaces::srv::rosidl_typesupport_c::DemuxList_service_type_support_handle;
}

#ifdef __cplusplus
}
#endif
