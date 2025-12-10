// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from topic_tools_interfaces:srv/DemuxSelect.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "topic_tools_interfaces/srv/demux_select.hpp"


#ifndef TOPIC_TOOLS_INTERFACES__SRV__DETAIL__DEMUX_SELECT__STRUCT_HPP_
#define TOPIC_TOOLS_INTERFACES__SRV__DETAIL__DEMUX_SELECT__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__topic_tools_interfaces__srv__DemuxSelect_Request __attribute__((deprecated))
#else
# define DEPRECATED__topic_tools_interfaces__srv__DemuxSelect_Request __declspec(deprecated)
#endif

namespace topic_tools_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct DemuxSelect_Request_
{
  using Type = DemuxSelect_Request_<ContainerAllocator>;

  explicit DemuxSelect_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->topic = "";
    }
  }

  explicit DemuxSelect_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : topic(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->topic = "";
    }
  }

  // field types and members
  using _topic_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _topic_type topic;

  // setters for named parameter idiom
  Type & set__topic(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->topic = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    topic_tools_interfaces::srv::DemuxSelect_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const topic_tools_interfaces::srv::DemuxSelect_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<topic_tools_interfaces::srv::DemuxSelect_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<topic_tools_interfaces::srv::DemuxSelect_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      topic_tools_interfaces::srv::DemuxSelect_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<topic_tools_interfaces::srv::DemuxSelect_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      topic_tools_interfaces::srv::DemuxSelect_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<topic_tools_interfaces::srv::DemuxSelect_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<topic_tools_interfaces::srv::DemuxSelect_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<topic_tools_interfaces::srv::DemuxSelect_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__topic_tools_interfaces__srv__DemuxSelect_Request
    std::shared_ptr<topic_tools_interfaces::srv::DemuxSelect_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__topic_tools_interfaces__srv__DemuxSelect_Request
    std::shared_ptr<topic_tools_interfaces::srv::DemuxSelect_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const DemuxSelect_Request_ & other) const
  {
    if (this->topic != other.topic) {
      return false;
    }
    return true;
  }
  bool operator!=(const DemuxSelect_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct DemuxSelect_Request_

// alias to use template instance with default allocator
using DemuxSelect_Request =
  topic_tools_interfaces::srv::DemuxSelect_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace topic_tools_interfaces


#ifndef _WIN32
# define DEPRECATED__topic_tools_interfaces__srv__DemuxSelect_Response __attribute__((deprecated))
#else
# define DEPRECATED__topic_tools_interfaces__srv__DemuxSelect_Response __declspec(deprecated)
#endif

namespace topic_tools_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct DemuxSelect_Response_
{
  using Type = DemuxSelect_Response_<ContainerAllocator>;

  explicit DemuxSelect_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->prev_topic = "";
      this->success = false;
    }
  }

  explicit DemuxSelect_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : prev_topic(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->prev_topic = "";
      this->success = false;
    }
  }

  // field types and members
  using _prev_topic_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _prev_topic_type prev_topic;
  using _success_type =
    bool;
  _success_type success;

  // setters for named parameter idiom
  Type & set__prev_topic(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->prev_topic = _arg;
    return *this;
  }
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    topic_tools_interfaces::srv::DemuxSelect_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const topic_tools_interfaces::srv::DemuxSelect_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<topic_tools_interfaces::srv::DemuxSelect_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<topic_tools_interfaces::srv::DemuxSelect_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      topic_tools_interfaces::srv::DemuxSelect_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<topic_tools_interfaces::srv::DemuxSelect_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      topic_tools_interfaces::srv::DemuxSelect_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<topic_tools_interfaces::srv::DemuxSelect_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<topic_tools_interfaces::srv::DemuxSelect_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<topic_tools_interfaces::srv::DemuxSelect_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__topic_tools_interfaces__srv__DemuxSelect_Response
    std::shared_ptr<topic_tools_interfaces::srv::DemuxSelect_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__topic_tools_interfaces__srv__DemuxSelect_Response
    std::shared_ptr<topic_tools_interfaces::srv::DemuxSelect_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const DemuxSelect_Response_ & other) const
  {
    if (this->prev_topic != other.prev_topic) {
      return false;
    }
    if (this->success != other.success) {
      return false;
    }
    return true;
  }
  bool operator!=(const DemuxSelect_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct DemuxSelect_Response_

// alias to use template instance with default allocator
using DemuxSelect_Response =
  topic_tools_interfaces::srv::DemuxSelect_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace topic_tools_interfaces


// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__topic_tools_interfaces__srv__DemuxSelect_Event __attribute__((deprecated))
#else
# define DEPRECATED__topic_tools_interfaces__srv__DemuxSelect_Event __declspec(deprecated)
#endif

namespace topic_tools_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct DemuxSelect_Event_
{
  using Type = DemuxSelect_Event_<ContainerAllocator>;

  explicit DemuxSelect_Event_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : info(_init)
  {
    (void)_init;
  }

  explicit DemuxSelect_Event_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : info(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _info_type =
    service_msgs::msg::ServiceEventInfo_<ContainerAllocator>;
  _info_type info;
  using _request_type =
    rosidl_runtime_cpp::BoundedVector<topic_tools_interfaces::srv::DemuxSelect_Request_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<topic_tools_interfaces::srv::DemuxSelect_Request_<ContainerAllocator>>>;
  _request_type request;
  using _response_type =
    rosidl_runtime_cpp::BoundedVector<topic_tools_interfaces::srv::DemuxSelect_Response_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<topic_tools_interfaces::srv::DemuxSelect_Response_<ContainerAllocator>>>;
  _response_type response;

  // setters for named parameter idiom
  Type & set__info(
    const service_msgs::msg::ServiceEventInfo_<ContainerAllocator> & _arg)
  {
    this->info = _arg;
    return *this;
  }
  Type & set__request(
    const rosidl_runtime_cpp::BoundedVector<topic_tools_interfaces::srv::DemuxSelect_Request_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<topic_tools_interfaces::srv::DemuxSelect_Request_<ContainerAllocator>>> & _arg)
  {
    this->request = _arg;
    return *this;
  }
  Type & set__response(
    const rosidl_runtime_cpp::BoundedVector<topic_tools_interfaces::srv::DemuxSelect_Response_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<topic_tools_interfaces::srv::DemuxSelect_Response_<ContainerAllocator>>> & _arg)
  {
    this->response = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    topic_tools_interfaces::srv::DemuxSelect_Event_<ContainerAllocator> *;
  using ConstRawPtr =
    const topic_tools_interfaces::srv::DemuxSelect_Event_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<topic_tools_interfaces::srv::DemuxSelect_Event_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<topic_tools_interfaces::srv::DemuxSelect_Event_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      topic_tools_interfaces::srv::DemuxSelect_Event_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<topic_tools_interfaces::srv::DemuxSelect_Event_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      topic_tools_interfaces::srv::DemuxSelect_Event_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<topic_tools_interfaces::srv::DemuxSelect_Event_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<topic_tools_interfaces::srv::DemuxSelect_Event_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<topic_tools_interfaces::srv::DemuxSelect_Event_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__topic_tools_interfaces__srv__DemuxSelect_Event
    std::shared_ptr<topic_tools_interfaces::srv::DemuxSelect_Event_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__topic_tools_interfaces__srv__DemuxSelect_Event
    std::shared_ptr<topic_tools_interfaces::srv::DemuxSelect_Event_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const DemuxSelect_Event_ & other) const
  {
    if (this->info != other.info) {
      return false;
    }
    if (this->request != other.request) {
      return false;
    }
    if (this->response != other.response) {
      return false;
    }
    return true;
  }
  bool operator!=(const DemuxSelect_Event_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct DemuxSelect_Event_

// alias to use template instance with default allocator
using DemuxSelect_Event =
  topic_tools_interfaces::srv::DemuxSelect_Event_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace topic_tools_interfaces

namespace topic_tools_interfaces
{

namespace srv
{

struct DemuxSelect
{
  using Request = topic_tools_interfaces::srv::DemuxSelect_Request;
  using Response = topic_tools_interfaces::srv::DemuxSelect_Response;
  using Event = topic_tools_interfaces::srv::DemuxSelect_Event;
};

}  // namespace srv

}  // namespace topic_tools_interfaces

#endif  // TOPIC_TOOLS_INTERFACES__SRV__DETAIL__DEMUX_SELECT__STRUCT_HPP_
