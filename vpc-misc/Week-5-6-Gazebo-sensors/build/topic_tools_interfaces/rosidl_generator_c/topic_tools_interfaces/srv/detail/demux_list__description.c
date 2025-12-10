// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from topic_tools_interfaces:srv/DemuxList.idl
// generated code does not contain a copyright notice

#include "topic_tools_interfaces/srv/detail/demux_list__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_topic_tools_interfaces
const rosidl_type_hash_t *
topic_tools_interfaces__srv__DemuxList__get_type_hash(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xb3, 0xe0, 0x38, 0xdb, 0xb7, 0xed, 0xce, 0x76,
      0x6e, 0x47, 0xe0, 0xc8, 0x97, 0x2b, 0x83, 0x7e,
      0x9a, 0x5d, 0x7f, 0xf1, 0x0d, 0x3e, 0x0d, 0x0f,
      0xc4, 0x08, 0x15, 0x65, 0xc4, 0x71, 0xb1, 0x44,
    }};
  return &hash;
}

ROSIDL_GENERATOR_C_PUBLIC_topic_tools_interfaces
const rosidl_type_hash_t *
topic_tools_interfaces__srv__DemuxList_Request__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x92, 0xd5, 0x4e, 0xb6, 0xb0, 0xba, 0x09, 0x22,
      0x43, 0xed, 0x12, 0x3c, 0x75, 0x3a, 0x0f, 0xdf,
      0x1f, 0x45, 0xa5, 0x38, 0x98, 0x58, 0xb8, 0x8a,
      0x00, 0x91, 0x2e, 0x43, 0x4c, 0x8b, 0xc1, 0x66,
    }};
  return &hash;
}

ROSIDL_GENERATOR_C_PUBLIC_topic_tools_interfaces
const rosidl_type_hash_t *
topic_tools_interfaces__srv__DemuxList_Response__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x40, 0x10, 0x16, 0x6e, 0x18, 0x68, 0xc2, 0x71,
      0x46, 0xed, 0x39, 0xbd, 0x02, 0xb2, 0xfb, 0x3f,
      0xdd, 0xf6, 0xa4, 0xf5, 0x2a, 0x2e, 0x8f, 0x26,
      0x26, 0x3c, 0x47, 0xd7, 0x07, 0x97, 0x04, 0x80,
    }};
  return &hash;
}

ROSIDL_GENERATOR_C_PUBLIC_topic_tools_interfaces
const rosidl_type_hash_t *
topic_tools_interfaces__srv__DemuxList_Event__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xe5, 0x8a, 0x4b, 0xdb, 0xf4, 0x1f, 0x43, 0xd9,
      0x29, 0xd9, 0xfc, 0x2b, 0xdc, 0xe1, 0x22, 0xb9,
      0x35, 0x1c, 0xd7, 0xc4, 0xd9, 0xcb, 0xd7, 0x69,
      0x66, 0xf3, 0x1f, 0x15, 0x49, 0x7b, 0x0a, 0x7e,
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

static char topic_tools_interfaces__srv__DemuxList__TYPE_NAME[] = "topic_tools_interfaces/srv/DemuxList";
static char builtin_interfaces__msg__Time__TYPE_NAME[] = "builtin_interfaces/msg/Time";
static char service_msgs__msg__ServiceEventInfo__TYPE_NAME[] = "service_msgs/msg/ServiceEventInfo";
static char topic_tools_interfaces__srv__DemuxList_Event__TYPE_NAME[] = "topic_tools_interfaces/srv/DemuxList_Event";
static char topic_tools_interfaces__srv__DemuxList_Request__TYPE_NAME[] = "topic_tools_interfaces/srv/DemuxList_Request";
static char topic_tools_interfaces__srv__DemuxList_Response__TYPE_NAME[] = "topic_tools_interfaces/srv/DemuxList_Response";

// Define type names, field names, and default values
static char topic_tools_interfaces__srv__DemuxList__FIELD_NAME__request_message[] = "request_message";
static char topic_tools_interfaces__srv__DemuxList__FIELD_NAME__response_message[] = "response_message";
static char topic_tools_interfaces__srv__DemuxList__FIELD_NAME__event_message[] = "event_message";

static rosidl_runtime_c__type_description__Field topic_tools_interfaces__srv__DemuxList__FIELDS[] = {
  {
    {topic_tools_interfaces__srv__DemuxList__FIELD_NAME__request_message, 15, 15},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {topic_tools_interfaces__srv__DemuxList_Request__TYPE_NAME, 44, 44},
    },
    {NULL, 0, 0},
  },
  {
    {topic_tools_interfaces__srv__DemuxList__FIELD_NAME__response_message, 16, 16},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {topic_tools_interfaces__srv__DemuxList_Response__TYPE_NAME, 45, 45},
    },
    {NULL, 0, 0},
  },
  {
    {topic_tools_interfaces__srv__DemuxList__FIELD_NAME__event_message, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {topic_tools_interfaces__srv__DemuxList_Event__TYPE_NAME, 42, 42},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription topic_tools_interfaces__srv__DemuxList__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    {NULL, 0, 0},
  },
  {
    {service_msgs__msg__ServiceEventInfo__TYPE_NAME, 33, 33},
    {NULL, 0, 0},
  },
  {
    {topic_tools_interfaces__srv__DemuxList_Event__TYPE_NAME, 42, 42},
    {NULL, 0, 0},
  },
  {
    {topic_tools_interfaces__srv__DemuxList_Request__TYPE_NAME, 44, 44},
    {NULL, 0, 0},
  },
  {
    {topic_tools_interfaces__srv__DemuxList_Response__TYPE_NAME, 45, 45},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
topic_tools_interfaces__srv__DemuxList__get_type_description(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {topic_tools_interfaces__srv__DemuxList__TYPE_NAME, 36, 36},
      {topic_tools_interfaces__srv__DemuxList__FIELDS, 3, 3},
    },
    {topic_tools_interfaces__srv__DemuxList__REFERENCED_TYPE_DESCRIPTIONS, 5, 5},
  };
  if (!constructed) {
    assert(0 == memcmp(&builtin_interfaces__msg__Time__EXPECTED_HASH, builtin_interfaces__msg__Time__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[0].fields = builtin_interfaces__msg__Time__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&service_msgs__msg__ServiceEventInfo__EXPECTED_HASH, service_msgs__msg__ServiceEventInfo__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[1].fields = service_msgs__msg__ServiceEventInfo__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[2].fields = topic_tools_interfaces__srv__DemuxList_Event__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[3].fields = topic_tools_interfaces__srv__DemuxList_Request__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[4].fields = topic_tools_interfaces__srv__DemuxList_Response__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}
// Define type names, field names, and default values
static char topic_tools_interfaces__srv__DemuxList_Request__FIELD_NAME__structure_needs_at_least_one_member[] = "structure_needs_at_least_one_member";

static rosidl_runtime_c__type_description__Field topic_tools_interfaces__srv__DemuxList_Request__FIELDS[] = {
  {
    {topic_tools_interfaces__srv__DemuxList_Request__FIELD_NAME__structure_needs_at_least_one_member, 35, 35},
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
topic_tools_interfaces__srv__DemuxList_Request__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {topic_tools_interfaces__srv__DemuxList_Request__TYPE_NAME, 44, 44},
      {topic_tools_interfaces__srv__DemuxList_Request__FIELDS, 1, 1},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}
// Define type names, field names, and default values
static char topic_tools_interfaces__srv__DemuxList_Response__FIELD_NAME__topics[] = "topics";

static rosidl_runtime_c__type_description__Field topic_tools_interfaces__srv__DemuxList_Response__FIELDS[] = {
  {
    {topic_tools_interfaces__srv__DemuxList_Response__FIELD_NAME__topics, 6, 6},
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
topic_tools_interfaces__srv__DemuxList_Response__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {topic_tools_interfaces__srv__DemuxList_Response__TYPE_NAME, 45, 45},
      {topic_tools_interfaces__srv__DemuxList_Response__FIELDS, 1, 1},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}
// Define type names, field names, and default values
static char topic_tools_interfaces__srv__DemuxList_Event__FIELD_NAME__info[] = "info";
static char topic_tools_interfaces__srv__DemuxList_Event__FIELD_NAME__request[] = "request";
static char topic_tools_interfaces__srv__DemuxList_Event__FIELD_NAME__response[] = "response";

static rosidl_runtime_c__type_description__Field topic_tools_interfaces__srv__DemuxList_Event__FIELDS[] = {
  {
    {topic_tools_interfaces__srv__DemuxList_Event__FIELD_NAME__info, 4, 4},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {service_msgs__msg__ServiceEventInfo__TYPE_NAME, 33, 33},
    },
    {NULL, 0, 0},
  },
  {
    {topic_tools_interfaces__srv__DemuxList_Event__FIELD_NAME__request, 7, 7},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE_BOUNDED_SEQUENCE,
      1,
      0,
      {topic_tools_interfaces__srv__DemuxList_Request__TYPE_NAME, 44, 44},
    },
    {NULL, 0, 0},
  },
  {
    {topic_tools_interfaces__srv__DemuxList_Event__FIELD_NAME__response, 8, 8},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE_BOUNDED_SEQUENCE,
      1,
      0,
      {topic_tools_interfaces__srv__DemuxList_Response__TYPE_NAME, 45, 45},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription topic_tools_interfaces__srv__DemuxList_Event__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    {NULL, 0, 0},
  },
  {
    {service_msgs__msg__ServiceEventInfo__TYPE_NAME, 33, 33},
    {NULL, 0, 0},
  },
  {
    {topic_tools_interfaces__srv__DemuxList_Request__TYPE_NAME, 44, 44},
    {NULL, 0, 0},
  },
  {
    {topic_tools_interfaces__srv__DemuxList_Response__TYPE_NAME, 45, 45},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
topic_tools_interfaces__srv__DemuxList_Event__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {topic_tools_interfaces__srv__DemuxList_Event__TYPE_NAME, 42, 42},
      {topic_tools_interfaces__srv__DemuxList_Event__FIELDS, 3, 3},
    },
    {topic_tools_interfaces__srv__DemuxList_Event__REFERENCED_TYPE_DESCRIPTIONS, 4, 4},
  };
  if (!constructed) {
    assert(0 == memcmp(&builtin_interfaces__msg__Time__EXPECTED_HASH, builtin_interfaces__msg__Time__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[0].fields = builtin_interfaces__msg__Time__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&service_msgs__msg__ServiceEventInfo__EXPECTED_HASH, service_msgs__msg__ServiceEventInfo__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[1].fields = service_msgs__msg__ServiceEventInfo__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[2].fields = topic_tools_interfaces__srv__DemuxList_Request__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[3].fields = topic_tools_interfaces__srv__DemuxList_Response__get_type_description(NULL)->type_description.fields;
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
topic_tools_interfaces__srv__DemuxList__get_individual_type_description_source(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {topic_tools_interfaces__srv__DemuxList__TYPE_NAME, 36, 36},
    {srv_encoding, 3, 3},
    {toplevel_type_raw_source, 20, 20},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource *
topic_tools_interfaces__srv__DemuxList_Request__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {topic_tools_interfaces__srv__DemuxList_Request__TYPE_NAME, 44, 44},
    {implicit_encoding, 8, 8},
    {NULL, 0, 0},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource *
topic_tools_interfaces__srv__DemuxList_Response__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {topic_tools_interfaces__srv__DemuxList_Response__TYPE_NAME, 45, 45},
    {implicit_encoding, 8, 8},
    {NULL, 0, 0},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource *
topic_tools_interfaces__srv__DemuxList_Event__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {topic_tools_interfaces__srv__DemuxList_Event__TYPE_NAME, 42, 42},
    {implicit_encoding, 8, 8},
    {NULL, 0, 0},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
topic_tools_interfaces__srv__DemuxList__get_type_description_sources(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[6];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 6, 6};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *topic_tools_interfaces__srv__DemuxList__get_individual_type_description_source(NULL),
    sources[1] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    sources[2] = *service_msgs__msg__ServiceEventInfo__get_individual_type_description_source(NULL);
    sources[3] = *topic_tools_interfaces__srv__DemuxList_Event__get_individual_type_description_source(NULL);
    sources[4] = *topic_tools_interfaces__srv__DemuxList_Request__get_individual_type_description_source(NULL);
    sources[5] = *topic_tools_interfaces__srv__DemuxList_Response__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
topic_tools_interfaces__srv__DemuxList_Request__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *topic_tools_interfaces__srv__DemuxList_Request__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
topic_tools_interfaces__srv__DemuxList_Response__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *topic_tools_interfaces__srv__DemuxList_Response__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
topic_tools_interfaces__srv__DemuxList_Event__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[5];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 5, 5};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *topic_tools_interfaces__srv__DemuxList_Event__get_individual_type_description_source(NULL),
    sources[1] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    sources[2] = *service_msgs__msg__ServiceEventInfo__get_individual_type_description_source(NULL);
    sources[3] = *topic_tools_interfaces__srv__DemuxList_Request__get_individual_type_description_source(NULL);
    sources[4] = *topic_tools_interfaces__srv__DemuxList_Response__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}
