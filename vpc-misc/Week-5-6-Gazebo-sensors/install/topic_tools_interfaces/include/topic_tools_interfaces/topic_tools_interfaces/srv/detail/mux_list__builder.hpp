// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from topic_tools_interfaces:srv/MuxList.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "topic_tools_interfaces/srv/mux_list.hpp"


#ifndef TOPIC_TOOLS_INTERFACES__SRV__DETAIL__MUX_LIST__BUILDER_HPP_
#define TOPIC_TOOLS_INTERFACES__SRV__DETAIL__MUX_LIST__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "topic_tools_interfaces/srv/detail/mux_list__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace topic_tools_interfaces
{

namespace srv
{


}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::topic_tools_interfaces::srv::MuxList_Request>()
{
  return ::topic_tools_interfaces::srv::MuxList_Request(rosidl_runtime_cpp::MessageInitialization::ZERO);
}

}  // namespace topic_tools_interfaces


namespace topic_tools_interfaces
{

namespace srv
{

namespace builder
{

class Init_MuxList_Response_topics
{
public:
  Init_MuxList_Response_topics()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::topic_tools_interfaces::srv::MuxList_Response topics(::topic_tools_interfaces::srv::MuxList_Response::_topics_type arg)
  {
    msg_.topics = std::move(arg);
    return std::move(msg_);
  }

private:
  ::topic_tools_interfaces::srv::MuxList_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::topic_tools_interfaces::srv::MuxList_Response>()
{
  return topic_tools_interfaces::srv::builder::Init_MuxList_Response_topics();
}

}  // namespace topic_tools_interfaces


namespace topic_tools_interfaces
{

namespace srv
{

namespace builder
{

class Init_MuxList_Event_response
{
public:
  explicit Init_MuxList_Event_response(::topic_tools_interfaces::srv::MuxList_Event & msg)
  : msg_(msg)
  {}
  ::topic_tools_interfaces::srv::MuxList_Event response(::topic_tools_interfaces::srv::MuxList_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::topic_tools_interfaces::srv::MuxList_Event msg_;
};

class Init_MuxList_Event_request
{
public:
  explicit Init_MuxList_Event_request(::topic_tools_interfaces::srv::MuxList_Event & msg)
  : msg_(msg)
  {}
  Init_MuxList_Event_response request(::topic_tools_interfaces::srv::MuxList_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_MuxList_Event_response(msg_);
  }

private:
  ::topic_tools_interfaces::srv::MuxList_Event msg_;
};

class Init_MuxList_Event_info
{
public:
  Init_MuxList_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MuxList_Event_request info(::topic_tools_interfaces::srv::MuxList_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_MuxList_Event_request(msg_);
  }

private:
  ::topic_tools_interfaces::srv::MuxList_Event msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::topic_tools_interfaces::srv::MuxList_Event>()
{
  return topic_tools_interfaces::srv::builder::Init_MuxList_Event_info();
}

}  // namespace topic_tools_interfaces

#endif  // TOPIC_TOOLS_INTERFACES__SRV__DETAIL__MUX_LIST__BUILDER_HPP_
