'use client';

import { getConversations, getConversationByID } from '@/lib/api';
import { formatDate } from '@/lib/utils';
import React, { useEffect, useState } from 'react';
import { Table, Modal, Card, Collapse, Input, Button, Rate} from 'antd';
const { Panel } = Collapse;

// modal for review

interface ModalReviewProps {
  conversationid: string;
  isModalVisible: boolean;
  handleModalVisibility: (visible: boolean) => void;
}

const ModalReview = ({ conversationid, isModalVisible, handleModalVisibility }: ModalReviewProps) => {
  // const [isModalOpen, setIsModalOpen] = useState(false);
  // const openModal = () => {
  //   setIsModalOpen(true);
  // }
  
  // const closeModal = () => {
  //   setIsModalOpen(false);
  // }
  const [conversation, setConversation] = useState<Conversation | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  const [items, setItems] = useState<any[]>([]);

  // Get review
  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsLoading(true);
        const data = await getConversationByID(conversationid);
        setConversation(data);
        // 这里需要把data.conversation解析成为一个list
        const conversionData = JSON.parse(data.conversation);
        const messageArray = Object.keys(conversionData).map((key) => ({
          id: key,
          ...conversionData[key]
        })).slice(1);
        setItems( messageArray|| [])
      } catch (error) {
        setError(error instanceof Error ? new Error(error.message) : Error('An error occurred'));
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, [conversationid]);

  return (
    <Modal
      title="对话详情"
      centered
      open={isModalVisible}
      onCancel={() => handleModalVisibility(false)}
      footer={null}
      width="70%"
    >
      <div className="modal-content">
        <h2>对话ID: {conversationid}</h2>
        <p>用户名称: {conversation?.user_name}</p>
        <p>顾客信息: {conversation?.role_info ? conversation.role_info : "<顾客信息未知>"}</p>
        {/*<p>对话内容: {conversation?.conversation}</p>*/}
        {items.map((item, index) => (
            <Card key={index} title={`对话内容 ${index + 1}`} style={{marginBottom: 16}}>
              <p>{item.content}</p>
              {/* <Collapse> */}
                {/* <Panel header="添加评论" key="1"> */}
                <Rate allowHalf defaultValue={0} onChange={(value) => console.log(`Rated with value ${value}`)} />
                  <Input.TextArea rows={4} placeholder="输入评论"/>
                  <Button type="primary" style={{marginTop: 16}}>提交评论</Button>
                {/* </Panel> */}
              {/* </Collapse> */}
            </Card>
        ))}

      </div>
    </Modal>
  )
};


interface Conversation {
    id: string;
    user_name: string;
    conversation: string;
    created_at: string;
    updated_at: string;
    notes: string;
    deleted: number;
    role_info: string;
    label_score: number;
    label_text: string;
    label_from_user: string;
    label_created_at: string;
  }

export default function ConversationReview() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [isLoading, setIsLoading] = useState(true);
//   const [error, setError] = useState(null);
  const [error, setError] = useState<Error | null>(null);
  const [selectedConversationId, setSelectedConversationId] = useState<string | null>(null);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const handleModalVisibility = (visible:any) => {
    setIsModalVisible(visible);
  };

  // 你可能需要实现 handleDetailsAndScoring 函数来处理按钮点击事件
  function handleDetailsAndScoring(id: string) {
    // 这里可以是打开一个模态框，或者是页面跳转等逻辑
    setSelectedConversationId(id);
    setIsModalVisible(true);
    console.log('Handling details and scoring for:', id);
  }


  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsLoading(true);
        const data = await getConversations();
        setConversations(data);
      } catch (error) {
        setError(error instanceof Error ? new Error(error.message) : Error('An error occurred'));
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
    },
    {
      // title: 'User Name',
      title: '用户名称',
      dataIndex: 'user_name',
      key: 'user_name',
    },
    // {
    //   title: '对话内容',
    //   dataIndex: 'conversation',
    //   key: 'conversation',
    //   render: (text: string) => text.length > 20 ? `${text.substring(0, 20)}...` : text
    // },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (text: string) => formatDate(text),
      sorter: (a: Conversation, b: Conversation) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime(),
    },
    {
      title: '打分',
      dataIndex: 'label_score',
      key: 'label_score',
    },

    {
      title: '操作',
      key: 'action',
      render: (_: any, record: Conversation) => (
        <button onClick={() => handleDetailsAndScoring(record.id)}
        style={{ backgroundColor: 'blue', color: 'white', padding: '10px 20px', borderRadius: '5px', border: 'none', cursor: 'pointer' }}
        >
          打分</button>
      ),
    }

  ];

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error.message}</div>;
  }

  return (
    <>
    <h1>对话打分</h1>
    < Table dataSource={conversations} columns={columns} rowKey='id'/>
    {isModalVisible && (
      <ModalReview
        conversationid={selectedConversationId || ''}
        isModalVisible={isModalVisible}
        handleModalVisibility={handleModalVisibility}
      />
    )}
    </>
    
    );

}
