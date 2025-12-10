// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from topic_tools_interfaces:srv/MuxDelete.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "topic_tools_interfaces/srv/mux_delete.h"


#ifndef TOPIC_TOOLS_INTERFACES__SRV__DETAIL__MUX_DELETE__STRUCT_H_
#define TOPIC_TOOLS_INTERFACES__SRV__DETAIL__MUX_DELETE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'topic'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/MuxDelete in the package topic_tools_interfaces.
typedef struct topic_tools_interfaces__srv__MuxDelete_Request
{
  rosidl_runtime_c__String topic;
} topic_tools_interfaces__srv__MuxDelete_Request;

// Struct for a sequence of topic_tools_interfaces__srv__MuxDelete_Request.
typedef struct topic_tools_interfaces__srv__MuxDelete_Request__Sequence
{
  topic_tools_interfaces__srv__MuxDelete_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} topic_tools_interfaces__srv__MuxDelete_Request__Sequence;

// Constants defined in the message

/// Struct defined in srv/MuxDelete in the package topic_tools_interfaces.
typedef struct topic_tools_interfaces__srv__MuxDelete_Response
{
  bool success;
} topic_tools_interfaces__srv__MuxDelete_Response;

// Struct for a sequence of topic_tools_interfaces__srv__MuxDelete_Response.
typedef struct topic_tools_interfaces__srv__MuxDelete_Response__Sequence
{
  topic_tools_interfaces__srv__MuxDelete_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} topic_tools_interfaces__srv__MuxDelete_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  topic_tools_interfaces__srv__MuxDelete_Event__request__MAX_SIZE = 1
};
// response
enum
{
  topic_tools_interfaces__srv__MuxDelete_Event__response__MAX_SIZE = 1
};

/// Struct defined in srv/MuxDelete in the package topic_tools_interfaces.
typedef struct topic_tools_interfaces__srv__MuxDelete_Event
{
  service_msgs__msg__ServiceEventInfo info;
  topic_tools_interfaces__srv__MuxDelete_Request__Sequence request;
  topic_tools_interfaces__srv__MuxDelete_Response__Sequence response;
} topic_tools_interfaces__srv__MuxDelete_Event;

// Struct for a sequence of topic_tools_interfaces__srv__MuxDelete_Event.
typedef struct topic_tools_interfaces__srv__MuxDelete_Event__Sequence
{
  topic_tools_interfaces__srv__MuxDelete_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} topic_tools_interfaces__srv__MuxDelete_Event__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // TOPIC_TOOLS_INTERFACES__SRV__DETAIL__MUX_DELETE__STRUCT_H_
