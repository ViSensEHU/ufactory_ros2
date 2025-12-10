// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from topic_tools_interfaces:srv/DemuxAdd.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "topic_tools_interfaces/srv/demux_add.hpp"


#ifndef TOPIC_TOOLS_INTERFACES__SRV__DETAIL__DEMUX_ADD__BUILDER_HPP_
#define TOPIC_TOOLS_INTERFACES__SRV__DETAIL__DEMUX_ADD__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "topic_tools_interfaces/srv/detail/demux_add__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace topic_tools_interfaces
{

namespace srv
{

namespace builder
{

class Init_DemuxAdd_Request_topic
{
public:
  Init_DemuxAdd_Request_topic()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::topic_tools_interfaces::srv::DemuxAdd_Request topic(::topic_tools_interfaces::srv::DemuxAdd_Request::_topic_type arg)
  {
    msg_.topic = std::move(arg);
    return std::move(msg_);
  }

private:
  ::topic_tools_interfaces::srv::DemuxAdd_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::topic_tools_interfaces::srv::DemuxAdd_Request>()
{
  return topic_tools_interfaces::srv::builder::Init_DemuxAdd_Request_topic();
}

}  // namespace topic_tools_interfaces


namespace topic_tools_interfaces
{

namespace srv
{

namespace builder
{

class Init_DemuxAdd_Response_success
{
public:
  Init_DemuxAdd_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::topic_tools_interfaces::srv::DemuxAdd_Response success(::topic_tools_interfaces::srv::DemuxAdd_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return std::move(msg_);
  }

private:
  ::topic_tools_interfaces::srv::DemuxAdd_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::topic_tools_interfaces::srv::DemuxAdd_Response>()
{
  return topic_tools_interfaces::srv::builder::Init_DemuxAdd_Response_success();
}

}  // namespace topic_tools_interfaces


namespace topic_tools_interfaces
{

namespace srv
{

namespace builder
{

class Init_DemuxAdd_Event_response
{
public:
  explicit Init_DemuxAdd_Event_response(::topic_tools_interfaces::srv::DemuxAdd_Event & msg)
  : msg_(msg)
  {}
  ::topic_tools_interfaces::srv::DemuxAdd_Event response(::topic_tools_interfaces::srv::DemuxAdd_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::topic_tools_interfaces::srv::DemuxAdd_Event msg_;
};

class Init_DemuxAdd_Event_request
{
public:
  explicit Init_DemuxAdd_Event_request(::topic_tools_interfaces::srv::DemuxAdd_Event & msg)
  : msg_(msg)
  {}
  Init_DemuxAdd_Event_response request(::topic_tools_interfaces::srv::DemuxAdd_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_DemuxAdd_Event_response(msg_);
  }

private:
  ::topic_tools_interfaces::srv::DemuxAdd_Event msg_;
};

class Init_DemuxAdd_Event_info
{
public:
  Init_DemuxAdd_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_DemuxAdd_Event_request info(::topic_tools_interfaces::srv::DemuxAdd_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_DemuxAdd_Event_request(msg_);
  }

private:
  ::topic_tools_interfaces::srv::DemuxAdd_Event msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::topic_tools_interfaces::srv::DemuxAdd_Event>()
{
  return topic_tools_interfaces::srv::builder::Init_DemuxAdd_Event_info();
}

}  // namespace topic_tools_interfaces

#endif  // TOPIC_TOOLS_INTERFACES__SRV__DETAIL__DEMUX_ADD__BUILDER_HPP_
