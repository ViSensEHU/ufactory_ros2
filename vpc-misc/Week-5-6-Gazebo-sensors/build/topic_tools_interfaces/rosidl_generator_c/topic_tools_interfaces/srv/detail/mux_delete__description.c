// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from topic_tools_interfaces:srv/MuxDelete.idl
// generated code does not contain a copyright notice

#include "topic_tools_interfaces/srv/detail/mux_delete__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_topic_tools_interfaces
const rosidl_type_hash_t *
topic_tools_interfaces__srv__MuxDelete__get_type_hash(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xeb, 0x9c, 0x4e, 0x4e, 0x4f, 0xd6, 0x07, 0x0d,
      0x94, 0xce, 0xb7, 0x38, 0x7d, 0xea, 0xeb, 0x93,
      0x81, 0x77, 0xc2, 0x83, 0xeb, 0x7b, 0x61, 0x34,
      0x07, 0xd5, 0xfd, 0xb9, 0xc7, 0xa7, 0xc4, 0xf7,
    }};
  return &hash;
}

ROSIDL_GENERATOR_C_PUBLIC_topic_tools_interfaces
const rosidl_type_hash_t *
topic_tools_interfaces__srv__MuxDelete_Request__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xc6, 0x4e, 0xf8, 0x81, 0xf0, 0x14, 0x66, 0x11,
      0x95, 0x72, 0xa4, 0xa4, 0xb4, 0xb4, 0xe4, 0x70,
      0x62, 0xbe, 0xe0, 0x1d, 0x36, 0x1a, 0x86, 0x73,
      0x63, 0xdb, 0xd4, 0x33, 0x51, 0xdc, 0x66, 0xab,
    }};
  return &hash;
}

ROSIDL_GENERATOR_C_PUBLIC_topic_tools_interfaces
const rosidl_type_hash_t *
topic_tools_interfaces__srv__MuxDelete_Response__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x28, 0xf1, 0x6e, 0x51, 0xcc, 0xb4, 0x16, 0x13,
      0x9f, 0x75, 0x25, 0x47, 0xdc, 0x27, 0x81, 0x6d,
      0xeb, 0xe7, 0xc5, 0xa7, 0x74, 0xbe, 0x7f, 0x88,
      0xa0, 0x2e, 0x44, 0x4e, 0x42, 0xae, 0xd4, 0xb1,
    }};
  return &hash;
}

ROSIDL_GENERATOR_C_PUBLIC_topic_tools_interfaces
const rosidl_type_hash_t *
topic_tools_interfaces__srv__MuxDelete_Event__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xe6, 0x3f, 0x4b, 0xdb, 0x70, 0xc2, 0x1e, 0xc8,
      0x99, 0xe7, 0xf2, 0xfd, 0x7e, 0xc6, 0x51, 0x3d,
      0xc1, 0x0b, 0x2b, 0x95, 0xf6, 0x7d, 0x5a, 0x96,
      0x00, 0x36, 0x10, 0xc4, 0xba, 0x2d, 0xa2, 0xf7,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types
#include "service_msgs/msg/detail/service_event_info__functions.h"
#include "builtin_interfaces/msg/detail/time__functions.h"

// Hashes for external referenced types
#ifndef NDEBUG
static const rosidl_type_hash_t builtin_interfaces__msg__Time__EXPECTED_HASH = {1, {
    0xb1, 0x06, 0x23, 0x5e, 0x25, 0xa4, 0xc5, 0xed,
    0x35, 0x09, 0x8a, 0xa0, 0xa6, 0x1a, 0x3e, 0xe9,
    0xc9, 0xb1, 0x8d, 0x19, 0x7f, 0x39, 0x8b, 0x0e,
    0x42, 0x06, 0xce, 0xa9, 0xac, 0xf9, 0xc1, 0x97,
  }};
static const rosidl_type_hash_t service_msgs__msg__ServiceEventInfo__EXPECTED_HASH = {1, {
    0x41, 0xbc, 0xbb, 0xe0, 0x7a, 0x75, 0xc9, 0xb5,
    0x2b, 0xc9, 0x6b, 0xfd, 0x5c, 0x24, 0xd7, 0xf0,
    0xfc, 0x0a, 0x08, 0xc0, 0xcb, 0x79, 0x21, 0xb3,
    0x37, 0x3c, 0x57, 0x32, 0x34, 0x5a, 0x6f, 0x45,
  }};
#endif

static char topic_tools_interfaces__srv__MuxDelete__TYPE_NAME[] = "topic_tools_interfaces/srv/MuxDelete";
static char builtin_interfaces__msg__Time__TYPE_NAME[] = "builtin_interfaces/msg/Time";
static char service_msgs__msg__ServiceEventInfo__TYPE_NAME[] = "service_msgs/msg/ServiceEventInfo";
static char topic_tools_interfaces__srv__MuxDelete_Event__TYPE_NAME[] = "topic_tools_interfaces/srv/MuxDelete_Event";
static char topic_tools_interfaces__srv__MuxDelete_Request__TYPE_NAME[] = "topic_tools_interfaces/srv/MuxDelete_Request";
static char topic_tools_interfaces__srv__MuxDelete_Response__TYPE_NAME[] = "topic_tools_interfaces/srv/MuxDelete_Response";

// Define type names, field names, and default values
static char topic_tools_interfaces__srv__MuxDelete__FIELD_NAME__request_message[] = "request_message";
static char topic_tools_interfaces__srv__MuxDelete__FIELD_NAME__response_message[] = "response_message";
static char topic_tools_interfaces__srv__MuxDelete__FIELD_NAME__event_message[] = "event_message";

static rosidl_runtime_c__type_description__Field topic_tools_interfaces__srv__MuxDelete__FIELDS[] = {
  {
    {topic_tools_interfaces__srv__MuxDelete__FIELD_NAME__request_message, 15, 15},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {topic_tools_interfaces__srv__MuxDelete_Request__TYPE_NAME, 44, 44},
    },
    {NULL, 0, 0},
  },
  {
    {topic_tools_interfaces__srv__MuxDelete__FIELD_NAME__response_message, 16, 16},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {topic_tools_interfaces__srv__MuxDelete_Response__TYPE_NAME, 45, 45},
    },
    {NULL, 0, 0},
  },
  {
    {topic_tools_interfaces__srv__MuxDelete__FIELD_NAME__event_message, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {topic_tools_interfaces__srv__MuxDelete_Event__TYPE_NAME, 42, 42},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription topic_tools_interfaces__srv__MuxDelete__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    {NULL, 0, 0},
  },
  {
    {service_msgs__msg__ServiceEventInfo__TYPE_NAME, 33, 33},
    {NULL, 0, 0},
  },
  {
    {topic_tools_interfaces__srv__MuxDelete_Event__TYPE_NAME, 42, 42},
    {NULL, 0, 0},
  },
  {
    {topic_tools_interfaces__srv__MuxDelete_Request__TYPE_NAME, 44, 44},
    {NULL, 0, 0},
  },
  {
    {topic_tools_interfaces__srv__MuxDelete_Response__TYPE_NAME, 45, 45},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
topic_tools_interfaces__srv__MuxDelete__get_type_description(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {topic_tools_interfaces__srv__MuxDelete__TYPE_NAME, 36, 36},
      {topic_tools_interfaces__srv__MuxDelete__FIELDS, 3, 3},
    },
    {topic_tools_interfaces__srv__MuxDelete__REFERENCED_TYPE_DESCRIPTIONS, 5, 5},
  };
  if (!constructed) {
    assert(0 == memcmp(&builtin_interfaces__msg__Time__EXPECTED_HASH, builtin_interfaces__msg__Time__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[0].fields = builtin_interfaces__msg__Time__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&service_msgs__msg__ServiceEventInfo__EXPECTED_HASH, service_msgs__msg__ServiceEventInfo__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[1].fields = service_msgs__msg__ServiceEventInfo__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[2].fields = topic_tools_interfaces__srv__MuxDelete_Event__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[3].fields = topic_tools_interfaces__srv__MuxDelete_Request__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[4].fields = topic_tools_interfaces__srv__MuxDelete_Response__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}
// Define type names, field names, and default values
static char topic_tools_interfaces__srv__MuxDelete_Request__FIELD_NAME__topic[] = "topic";

static rosidl_runtime_c__type_description__Field topic_tools_interfaces__srv__MuxDelete_Request__FIELDS[] = {
  {
    {topic_tools_interfaces__srv__MuxDelete_Request__FIELD_NAME__topic, 5, 5},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
topic_tools_interfaces__srv__MuxDelete_Request__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {topic_tools_interfaces__srv__MuxDelete_Request__TYPE_NAME, 44, 44},
      {topic_tools_interfaces__srv__MuxDelete_Request__FIELDS, 1, 1},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}
// Define type names, field names, and default values
static char topic_tools_interfaces__srv__MuxDelete_Response__FIELD_NAME__success[] = "success";

static rosidl_runtime_c__type_description__Field topic_tools_interfaces__srv__MuxDelete_Response__FIELDS[] = {
  {
    {topic_tools_interfaces__srv__MuxDelete_Response__FIELD_NAME__success, 7, 7},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
topic_tools_interfaces__srv__MuxDelete_Response__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {topic_tools_interfaces__srv__MuxDelete_Response__TYPE_NAME, 45, 45},
      {topic_tools_interfaces__srv__MuxDelete_Response__FIELDS, 1, 1},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}
// Define type names, field names, and default values
static char topic_tools_interfaces__srv__MuxDelete_Event__FIELD_NAME__info[] = "info";
static char topic_tools_interfaces__srv__MuxDelete_Event__FIELD_NAME__request[] = "request";
static char topic_tools_interfaces__srv__MuxDelete_Event__FIELD_NAME__response[] = "response";

static rosidl_runtime_c__type_description__Field topic_tools_interfaces__srv__MuxDelete_Event__FIELDS[] = {
  {
    {topic_tools_interfaces__srv__MuxDelete_Event__FIELD_NAME__info, 4, 4},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {service_msgs__msg__ServiceEventInfo__TYPE_NAME, 33, 33},
    },
    {NULL, 0, 0},
  },
  {
    {topic_tools_interfaces__srv__MuxDelete_Event__FIELD_NAME__request, 7, 7},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE_BOUNDED_SEQUENCE,
      1,
      0,
      {topic_tools_interfaces__srv__MuxDelete_Request__TYPE_NAME, 44, 44},
    },
    {NULL, 0, 0},
  },
  {
    {topic_tools_interfaces__srv__MuxDelete_Event__FIELD_NAME__response, 8, 8},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE_BOUNDED_SEQUENCE,
      1,
      0,
      {topic_tools_interfaces__srv__MuxDelete_Response__TYPE_NAME, 45, 45},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription topic_tools_interfaces__srv__MuxDelete_Event__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    {NULL, 0, 0},
  },
  {
    {service_msgs__msg__ServiceEventInfo__TYPE_NAME, 33, 33},
    {NULL, 0, 0},
  },
  {
    {topic_tools_interfaces__srv__MuxDelete_Request__TYPE_NAME, 44, 44},
    {NULL, 0, 0},
  },
  {
    {topic_tools_interfaces__srv__MuxDelete_Response__TYPE_NAME, 45, 45},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
topic_tools_interfaces__srv__MuxDelete_Event__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {topic_tools_interfaces__srv__MuxDelete_Event__TYPE_NAME, 42, 42},
      {topic_tools_interfaces__srv__MuxDelete_Event__FIELDS, 3, 3},
    },
    {topic_tools_interfaces__srv__MuxDelete_Event__REFERENCED_TYPE_DESCRIPTIONS, 4, 4},
  };
  if (!constructed) {
    assert(0 == memcmp(&builtin_interfaces__msg__Time__EXPECTED_HASH, builtin_interfaces__msg__Time__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[0].fields = builtin_interfaces__msg__Time__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&service_msgs__msg__ServiceEventInfo__EXPECTED_HASH, service_msgs__msg__ServiceEventInfo__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[1].fields = service_msgs__msg__ServiceEventInfo__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[2].fields = topic_tools_interfaces__srv__MuxDelete_Request__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[3].fields = topic_tools_interfaces__srv__MuxDelete_Response__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "string topic\n"
  "---\n"
  "bool success";

static char srv_encoding[] = "srv";
static char implicit_encoding[] = "implicit";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
topic_tools_interfaces__srv__MuxDelete__get_individual_type_description_source(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {topic_tools_interfaces__srv__MuxDelete__TYPE_NAME, 36, 36},
    {srv_encoding, 3, 3},
    {toplevel_type_raw_source, 30, 30},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource *
topic_tools_interfaces__srv__MuxDelete_Request__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {topic_tools_interfaces__srv__MuxDelete_Request__TYPE_NAME, 44, 44},
    {implicit_encoding, 8, 8},
    {NULL, 0, 0},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource *
topic_tools_interfaces__srv__MuxDelete_Response__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {topic_tools_interfaces__srv__MuxDelete_Response__TYPE_NAME, 45, 45},
    {implicit_encoding, 8, 8},
    {NULL, 0, 0},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource *
topic_tools_interfaces__srv__MuxDelete_Event__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {topic_tools_interfaces__srv__MuxDelete_Event__TYPE_NAME, 42, 42},
    {implicit_encoding, 8, 8},
    {NULL, 0, 0},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
topic_tools_interfaces__srv__MuxDelete__get_type_description_sources(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[6];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 6, 6};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *topic_tools_interfaces__srv__MuxDelete__get_individual_type_description_source(NULL),
    sources[1] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    sources[2] = *service_msgs__msg__ServiceEventInfo__get_individual_type_description_source(NULL);
    sources[3] = *topic_tools_interfaces__srv__MuxDelete_Event__get_individual_type_description_source(NULL);
    sources[4] = *topic_tools_interfaces__srv__MuxDelete_Request__get_individual_type_description_source(NULL);
    sources[5] = *topic_tools_interfaces__srv__MuxDelete_Response__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
topic_tools_interfaces__srv__MuxDelete_Request__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *topic_tools_interfaces__srv__MuxDelete_Request__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
topic_tools_interfaces__srv__MuxDelete_Response__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *topic_tools_interfaces__srv__MuxDelete_Response__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
topic_tools_interfaces__srv__MuxDelete_Event__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[5];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 5, 5};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *topic_tools_interfaces__srv__MuxDelete_Event__get_individual_type_description_source(NULL),
    sources[1] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    sources[2] = *service_msgs__msg__ServiceEventInfo__get_individual_type_description_source(NULL);
    sources[3] = *topic_tools_interfaces__srv__MuxDelete_Request__get_individual_type_description_source(NULL);
    sources[4] = *topic_tools_interfaces__srv__MuxDelete_Response__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}
