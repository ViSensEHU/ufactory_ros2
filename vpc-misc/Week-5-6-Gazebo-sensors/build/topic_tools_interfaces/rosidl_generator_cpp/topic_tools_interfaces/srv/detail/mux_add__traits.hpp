// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from topic_tools_interfaces:srv/MuxAdd.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "topic_tools_interfaces/srv/mux_add.hpp"


#ifndef TOPIC_TOOLS_INTERFACES__SRV__DETAIL__MUX_ADD__TRAITS_HPP_
#define TOPIC_TOOLS_INTERFACES__SRV__DETAIL__MUX_ADD__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "topic_tools_interfaces/srv/detail/mux_add__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace topic_tools_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const MuxAdd_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: topic
  {
    out << "topic: ";
    rosidl_generator_traits::value_to_yaml(msg.topic, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MuxAdd_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: topic
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "topic: ";
    rosidl_generator_traits::value_to_yaml(msg.topic, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MuxAdd_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace topic_tools_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use topic_tools_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const topic_tools_interfaces::srv::MuxAdd_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  topic_tools_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use topic_tools_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const topic_tools_interfaces::srv::MuxAdd_Request & msg)
{
  return topic_tools_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<topic_tools_interfaces::srv::MuxAdd_Request>()
{
  return "topic_tools_interfaces::srv::MuxAdd_Request";
}

template<>
inline const char * name<topic_tools_interfaces::srv::MuxAdd_Request>()
{
  return "topic_tools_interfaces/srv/MuxAdd_Request";
}

template<>
struct has_fixed_size<topic_tools_interfaces::srv::MuxAdd_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<topic_tools_interfaces::srv::MuxAdd_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<topic_tools_interfaces::srv::MuxAdd_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace topic_tools_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const MuxAdd_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MuxAdd_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MuxAdd_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace topic_tools_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use topic_tools_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const topic_tools_interfaces::srv::MuxAdd_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  topic_tools_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use topic_tools_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const topic_tools_interfaces::srv::MuxAdd_Response & msg)
{
  return topic_tools_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<topic_tools_interfaces::srv::MuxAdd_Response>()
{
  return "topic_tools_interfaces::srv::MuxAdd_Response";
}

template<>
inline const char * name<topic_tools_interfaces::srv::MuxAdd_Response>()
{
  return "topic_tools_interfaces/srv/MuxAdd_Response";
}

template<>
struct has_fixed_size<topic_tools_interfaces::srv::MuxAdd_Response>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<topic_tools_interfaces::srv::MuxAdd_Response>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<topic_tools_interfaces::srv::MuxAdd_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__traits.hpp"

namespace topic_tools_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const MuxAdd_Event & msg,
  std::ostream & out)
{
  out << "{";
  // member: info
  {
    out << "info: ";
    to_flow_style_yaml(msg.info, out);
    out << ", ";
  }

  // member: request
  {
    if (msg.request.size() == 0) {
      out << "request: []";
    } else {
      out << "request: [";
      size_t pending_items = msg.request.size();
      for (auto item : msg.request) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: response
  {
    if (msg.response.size() == 0) {
      out << "response: []";
    } else {
      out << "response: [";
      size_t pending_items = msg.response.size();
      for (auto item : msg.response) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MuxAdd_Event & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: info
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "info:\n";
    to_block_style_yaml(msg.info, out, indentation + 2);
  }

  // member: request
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.request.size() == 0) {
      out << "request: []\n";
    } else {
      out << "request:\n";
      for (auto item : msg.request) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: response
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.response.size() == 0) {
      out << "response: []\n";
    } else {
      out << "response:\n";
      for (auto item : msg.response) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MuxAdd_Event & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace topic_tools_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use topic_tools_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const topic_tools_interfaces::srv::MuxAdd_Event & msg,
  std::ostream & out, size_t indentation = 0)
{
  topic_tools_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use topic_tools_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const topic_tools_interfaces::srv::MuxAdd_Event & msg)
{
  return topic_tools_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<topic_tools_interfaces::srv::MuxAdd_Event>()
{
  return "topic_tools_interfaces::srv::MuxAdd_Event";
}

template<>
inline const char * name<topic_tools_interfaces::srv::MuxAdd_Event>()
{
  return "topic_tools_interfaces/srv/MuxAdd_Event";
}

template<>
struct has_fixed_size<topic_tools_interfaces::srv::MuxAdd_Event>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<topic_tools_interfaces::srv::MuxAdd_Event>
  : std::integral_constant<bool, has_bounded_size<service_msgs::msg::ServiceEventInfo>::value && has_bounded_size<topic_tools_interfaces::srv::MuxAdd_Request>::value && has_bounded_size<topic_tools_interfaces::srv::MuxAdd_Response>::value> {};

template<>
struct is_message<topic_tools_interfaces::srv::MuxAdd_Event>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<topic_tools_interfaces::srv::MuxAdd>()
{
  return "topic_tools_interfaces::srv::MuxAdd";
}

template<>
inline const char * name<topic_tools_interfaces::srv::MuxAdd>()
{
  return "topic_tools_interfaces/srv/MuxAdd";
}

template<>
struct has_fixed_size<topic_tools_interfaces::srv::MuxAdd>
  : std::integral_constant<
    bool,
    has_fixed_size<topic_tools_interfaces::srv::MuxAdd_Request>::value &&
    has_fixed_size<topic_tools_interfaces::srv::MuxAdd_Response>::value
  >
{
};

template<>
struct has_bounded_size<topic_tools_interfaces::srv::MuxAdd>
  : std::integral_constant<
    bool,
    has_bounded_size<topic_tools_interfaces::srv::MuxAdd_Request>::value &&
    has_bounded_size<topic_tools_interfaces::srv::MuxAdd_Response>::value
  >
{
};

template<>
struct is_service<topic_tools_interfaces::srv::MuxAdd>
  : std::true_type
{
};

template<>
struct is_service_request<topic_tools_interfaces::srv::MuxAdd_Request>
  : std::true_type
{
};

template<>
struct is_service_response<topic_tools_interfaces::srv::MuxAdd_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // TOPIC_TOOLS_INTERFACES__SRV__DETAIL__MUX_ADD__TRAITS_HPP_
