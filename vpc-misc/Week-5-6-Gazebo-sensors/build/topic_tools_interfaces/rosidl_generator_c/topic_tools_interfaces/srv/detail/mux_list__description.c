// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from topic_tools_interfaces:srv/MuxList.idl
// generated code does not contain a copyright notice

#include "topic_tools_interfaces/srv/detail/mux_list__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_topic_tools_interfaces
const rosidl_type_hash_t *
topic_tools_interfaces__srv__MuxList__get_type_hash(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xd1, 0xde, 0xad, 0x37, 0xea, 0xe2, 0xc9, 0x28,
      0x91, 0xd8, 0xb9, 0x7d, 0x4f, 0xb0, 0x50, 0x4f,
      0x02, 0xfd, 0xa8, 0x93, 0xbc, 0x2d, 0x67, 0x00,
      0x6b, 0xf7, 0xc3, 0x47, 0xeb, 0x8c, 0xa5, 0x4f,
    }};
  return &hash;
}

ROSIDL_GENERATOR_C_PUBLIC_topic_tools_interfaces
const rosidl_type_hash_t *
topic_tools_interfaces__srv__MuxList_Request__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x94, 0x84, 0xc1, 0x05, 0xac, 0x76, 0x60, 0xde,
      0x44, 0x9a, 0x5f, 0x4e, 0xef, 0x7a, 0x31, 0x29,
      0x6d, 0x31, 0x89, 0x4f, 0xcd, 0x7b, 0x17, 0x17,
      0xa4, 0xf5, 0xe7, 0x4f, 0xc4, 0xe5, 0x04, 0x7a,
    }};
  return &hash;
}

ROSIDL_GENERATOR_C_PUBLIC_topic_tools_interfaces
const rosidl_type_hash_t *
topic_tools_interfaces__srv__MuxList_Response__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xf4, 0xc8, 0x6e, 0xae, 0x78, 0xd9, 0xc9, 0x8c,
      0x9a, 0xfd, 0x4d, 0x3f, 0x49, 0x6b, 0xbb, 0x73,
      0x61, 0x9d, 0x97, 0x64, 0x5c, 0x45, 0xe4, 0x59,
      0x44, 0x38, 0x0d, 0x4d, 0x9a, 0xac, 0x9e, 0xe6,
    }};
  return &hash;
}

ROSIDL_GENERATOR_C_PUBLIC_topic_tools_interfaces
const rosidl_type_hash_t *
topic_tools_interfaces__srv__MuxList_Event__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x8c, 0xb1, 0x8a, 0x46, 0xa3, 0x1b, 0x90, 0x71,
      0x78, 0xce, 0xbc, 0x84, 0x8c, 0x75, 0xd7, 0x49,
      0xc0, 0xcd, 0xcf, 0x0e, 0x4d, 0xf8, 0x2d, 0xeb,
      0x5f, 0xe8, 0x75, 0xc1, 0xe1, 0xbe, 0x8c, 0x6e,
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

static char topic_tools_interfaces__srv__MuxList__TYPE_NAME[] = "topic_tools_interfaces/srv/MuxList";
static char builtin_interfaces__msg__Time__TYPE_NAME[] = "builtin_interfaces/msg/Time";
static char service_msgs__msg__ServiceEventInfo__TYPE_NAME[] = "service_msgs/msg/ServiceEventInfo";
static char topic_tools_interfaces__srv__MuxList_Event__TYPE_NAME[] = "topic_tools_interfaces/srv/MuxList_Event";
static char topic_tools_interfaces__srv__MuxList_Request__TYPE_NAME[] = "topic_tools_interfaces/srv/MuxList_Request";
static char topic_tools_interfaces__srv__MuxList_Response__TYPE_NAME[] = "topic_tools_interfaces/srv/MuxList_Response";

// Define type names, field names, and default values
static char topic_tools_interfaces__srv__MuxList__FIELD_NAME__request_message[] = "request_message";
static char topic_tools_interfaces__srv__MuxList__FIELD_NAME__response_message[] = "response_message";
static char topic_tools_interfaces__srv__MuxList__FIELD_NAME__event_message[] = "event_message";

static rosidl_runtime_c__type_description__Field topic_tools_interfaces__srv__MuxList__FIELDS[] = {
  {
    {topic_tools_interfaces__srv__MuxList__FIELD_NAME__request_message, 15, 15},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {topic_tools_interfaces__srv__MuxList_Request__TYPE_NAME, 42, 42},
    },
    {NULL, 0, 0},
  },
  {
    {topic_tools_interfaces__srv__MuxList__FIELD_NAME__response_message, 16, 16},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {topic_tools_interfaces__srv__MuxList_Response__TYPE_NAME, 43, 43},
    },
    {NULL, 0, 0},
  },
  {
    {topic_tools_interfaces__srv__MuxList__FIELD_NAME__event_message, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {topic_tools_interfaces__srv__MuxList_Event__TYPE_NAME, 40, 40},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription topic_tools_interfaces__srv__MuxList__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    {NULL, 0, 0},
  },
  {
    {service_msgs__msg__ServiceEventInfo__TYPE_NAME, 33, 33},
    {NULL, 0, 0},
  },
  {
    {topic_tools_interfaces__srv__MuxList_Event__TYPE_NAME, 40, 40},
    {NULL, 0, 0},
  },
  {
    {topic_tools_interfaces__srv__MuxList_Request__TYPE_NAME, 42, 42},
    {NULL, 0, 0},
  },
  {
    {topic_tools_interfaces__srv__MuxList_Response__TYPE_NAME, 43, 43},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
topic_tools_interfaces__srv__MuxList__get_type_description(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {topic_tools_interfaces__srv__MuxList__TYPE_NAME, 34, 34},
      {topic_tools_interfaces__srv__MuxList__FIELDS, 3, 3},
    },
    {topic_tools_interfaces__srv__MuxList__REFERENCED_TYPE_DESCRIPTIONS, 5, 5},
  };
  if (!constructed) {
    assert(0 == memcmp(&builtin_interfaces__msg__Time__EXPECTED_HASH, builtin_interfaces__msg__Time__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[0].fields = builtin_interfaces__msg__Time__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&service_msgs__msg__ServiceEventInfo__EXPECTED_HASH, service_msgs__msg__ServiceEventInfo__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[1].fields = service_msgs__msg__ServiceEventInfo__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[2].fields = topic_tools_interfaces__srv__MuxList_Event__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[3].fields = topic_tools_interfaces__srv__MuxList_Request__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[4].fields = topic_tools_interfaces__srv__MuxList_Response__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}
// Define type names, field names, and default values
static char topic_tools_interfaces__srv__MuxList_Request__FIELD_NAME__structure_needs_at_least_one_member[] = "structure_needs_at_least_one_member";

static rosidl_runtime_c__type_description__Field topic_tools_interfaces__srv__MuxList_Request__FIELDS[] = {
  {
    {topic_tools_interfaces__srv__MuxList_Request__FIELD_NAME__structure_needs_at_least_one_member, 35, 35},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT8,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
topic_tools_interfaces__srv__MuxList_Request__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {topic_tools_interfaces__srv__MuxList_Request__TYPE_NAME, 42, 42},
      {topic_tools_interfaces__srv__MuxList_Request__FIELDS, 1, 1},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}
// Define type names, field names, and default values
static char topic_tools_interfaces__srv__MuxList_Response__FIELD_NAME__topics[] = "topics";

static rosidl_runtime_c__type_description__Field topic_tools_interfaces__srv__MuxList_Response__FIELDS[] = {
  {
    {topic_tools_interfaces__srv__MuxList_Response__FIELD_NAME__topics, 6, 6},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING_UNBOUNDED_SEQUENCE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
topic_tools_interfaces__srv__MuxList_Response__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {topic_tools_interfaces__srv__MuxList_Response__TYPE_NAME, 43, 43},
      {topic_tools_interfaces__srv__MuxList_Response__FIELDS, 1, 1},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}
// Define type names, field names, and default values
static char topic_tools_interfaces__srv__MuxList_Event__FIELD_NAME__info[] = "info";
static char topic_tools_interfaces__srv__MuxList_Event__FIELD_NAME__request[] = "request";
static char topic_tools_interfaces__srv__MuxList_Event__FIELD_NAME__response[] = "response";

static rosidl_runtime_c__type_description__Field topic_tools_interfaces__srv__MuxList_Event__FIELDS[] = {
  {
    {topic_tools_interfaces__srv__MuxList_Event__FIELD_NAME__info, 4, 4},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {service_msgs__msg__ServiceEventInfo__TYPE_NAME, 33, 33},
    },
    {NULL, 0, 0},
  },
  {
    {topic_tools_interfaces__srv__MuxList_Event__FIELD_NAME__request, 7, 7},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE_BOUNDED_SEQUENCE,
      1,
      0,
      {topic_tools_interfaces__srv__MuxList_Request__TYPE_NAME, 42, 42},
    },
    {NULL, 0, 0},
  },
  {
    {topic_tools_interfaces__srv__MuxList_Event__FIELD_NAME__response, 8, 8},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE_BOUNDED_SEQUENCE,
      1,
      0,
      {topic_tools_interfaces__srv__MuxList_Response__TYPE_NAME, 43, 43},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription topic_tools_interfaces__srv__MuxList_Event__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    {NULL, 0, 0},
  },
  {
    {service_msgs__msg__ServiceEventInfo__TYPE_NAME, 33, 33},
    {NULL, 0, 0},
  },
  {
    {topic_tools_interfaces__srv__MuxList_Request__TYPE_NAME, 42, 42},
    {NULL, 0, 0},
  },
  {
    {topic_tools_interfaces__srv__MuxList_Response__TYPE_NAME, 43, 43},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
topic_tools_interfaces__srv__MuxList_Event__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {topic_tools_interfaces__srv__MuxList_Event__TYPE_NAME, 40, 40},
      {topic_tools_interfaces__srv__MuxList_Event__FIELDS, 3, 3},
    },
    {topic_tools_interfaces__srv__MuxList_Event__REFERENCED_TYPE_DESCRIPTIONS, 4, 4},
  };
  if (!constructed) {
    assert(0 == memcmp(&builtin_interfaces__msg__Time__EXPECTED_HASH, builtin_interfaces__msg__Time__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[0].fields = builtin_interfaces__msg__Time__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&service_msgs__msg__ServiceEventInfo__EXPECTED_HASH, service_msgs__msg__ServiceEventInfo__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[1].fields = service_msgs__msg__ServiceEventInfo__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[2].fields = topic_tools_interfaces__srv__MuxList_Request__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[3].fields = topic_tools_interfaces__srv__MuxList_Response__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "---\n"
  "string[] topics";

static char srv_encoding[] = "srv";
static char implicit_encoding[] = "implicit";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
topic_tools_interfaces__srv__MuxList__get_individual_type_description_source(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {topic_tools_interfaces__srv__MuxList__TYPE_NAME, 34, 34},
    {srv_encoding, 3, 3},
    {toplevel_type_raw_source, 20, 20},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource *
topic_tools_interfaces__srv__MuxList_Request__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {topic_tools_interfaces__srv__MuxList_Request__TYPE_NAME, 42, 42},
    {implicit_encoding, 8, 8},
    {NULL, 0, 0},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource *
topic_tools_interfaces__srv__MuxList_Response__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {topic_tools_interfaces__srv__MuxList_Response__TYPE_NAME, 43, 43},
    {implicit_encoding, 8, 8},
    {NULL, 0, 0},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource *
topic_tools_interfaces__srv__MuxList_Event__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {topic_tools_interfaces__srv__MuxList_Event__TYPE_NAME, 40, 40},
    {implicit_encoding, 8, 8},
    {NULL, 0, 0},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
topic_tools_interfaces__srv__MuxList__get_type_description_sources(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[6];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 6, 6};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *topic_tools_interfaces__srv__MuxList__get_individual_type_description_source(NULL),
    sources[1] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    sources[2] = *service_msgs__msg__ServiceEventInfo__get_individual_type_description_source(NULL);
    sources[3] = *topic_tools_interfaces__srv__MuxList_Event__get_individual_type_description_source(NULL);
    sources[4] = *topic_tools_interfaces__srv__MuxList_Request__get_individual_type_description_source(NULL);
    sources[5] = *topic_tools_interfaces__srv__MuxList_Response__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
topic_tools_interfaces__srv__MuxList_Request__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *topic_tools_interfaces__srv__MuxList_Request__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
topic_tools_interfaces__srv__MuxList_Response__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *topic_tools_interfaces__srv__MuxList_Response__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
topic_tools_interfaces__srv__MuxList_Event__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[5];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 5, 5};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *topic_tools_interfaces__srv__MuxList_Event__get_individual_type_description_source(NULL),
    sources[1] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    sources[2] = *service_msgs__msg__ServiceEventInfo__get_individual_type_description_source(NULL);
    sources[3] = *topic_tools_interfaces__srv__MuxList_Request__get_individual_type_description_source(NULL);
    sources[4] = *topic_tools_interfaces__srv__MuxList_Response__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}
