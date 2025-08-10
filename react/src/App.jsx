import { useState, useRef } from "react";
import axios from "axios";

function App() {
  // 定义内容状态，存储用户输入的提问内容
  const [content, setContent] = useState("");
  // 定义响应状态，存储服务器返回的提交结果信息
  const [response, setResponse] = useState("");
  // 创建对 textarea DOM 元素的引用，方便动态调整高度
  const textareaRef = useRef(null);

  // 当用户在 textarea 输入时触发此函数
  const handleInput = (e) => {
    const textarea = textareaRef.current;
    if (textarea) {
      // 重置高度，避免累加高度造成 textarea 越来越大
      textarea.style.height = "auto";
      // 根据内容的实际滚动高度动态调整 textarea 高度，实现自适应高度效果
      textarea.style.height = textarea.scrollHeight + "px";
    }
    // 更新状态 content，保持受控组件
    setContent(e.target.value);
  };

  // 点击提交按钮时触发的异步函数
  const handleSubmit = async () => {
    try {
      // 使用 axios 发送 POST 请求，将 content 作为 JSON 请求体发送到指定接口
      const res = await axios.post(
        "https://api.mineraltown.net/marshmallow",
        { content: content },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      // 请求成功，设置响应状态为服务器返回的 status 字段值
      setResponse(res.data.status);
    } catch (err) {
      // 如果请求失败，尝试从错误响应中提取详细错误信息
      if (err.response && err.response.data && err.response.data.detail) {
        setResponse(err.response.data.detail);
      } else {
        // 如果没有详细信息，显示通用错误信息
        setResponse("请求失败: " + err.message);
      }
    }
  };

  // 组件渲染内容
  return (
    <div style={{ padding: "20px", fontFamily: "sans-serif" }}>
      {/* 直播间 */}
      <a
        href="https://live.bilibili.com/3472667"
        className="live"
        target="_blank"
        rel="noopener noreferrer"
      >
        直播间
      </a>
      {/* 标题 */}
      <h1>起源の棉花糖</h1>
      {/* 用户输入区域 */}
      <textarea
        ref={textareaRef} // 绑定 DOM 引用，方便动态调整高度
        placeholder="请输入你的提问内容" // 默认提示
        value={content} // 受控组件：内容来自 content 状态
        onInput={handleInput} // 输入时调整高度
        onChange={(e) => setContent(e.target.value)} // 兼容 React 的状态更新，保持内容同步
      />
      <br />
      {/* 提交按钮 */}
      <button onClick={handleSubmit} style={{ marginTop: "10px" }}>
        提交
      </button>
      {/* 如果有响应结果，则显示对应信息 */}
      {response && (
        <div style={{ marginTop: "20px" }}>
          <h3
            style={{
              color: response === "提交成功" ? "#81c784" : "#e57373",
            }}
          >
            {response === "提交成功" ? "成功  " : "错误"}
          </h3>
          <pre
            style={{
              color: response === "提交成功" ? "#66bb6a" : "#ef9a9a",
            }}
          >
            {response != "提交成功" ? response : "棉花糖已经提交～"}
          </pre>
        </div>
      )}
    </div>
  );
}

export default App;
