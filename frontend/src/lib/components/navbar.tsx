
import React from 'react';
import { Menu, Layout } from 'antd';
// import { Link } from 'react-router-dom';
import Link from 'next/link';

const { Header } = Layout;

const Navbar = () => {
  return (
    <Header>
      <div className="logo" />
      <Menu theme="dark" mode="horizontal" defaultSelectedKeys={['1']}>
        <Menu.Item key="1">
            <Link href="/">首页</Link>
        </Menu.Item>
        <Menu.Item key="2">
            <Link href="conversation-review">对话评估</Link>
        </Menu.Item>
        {/* 更多菜单项 */}
      </Menu>
    </Header>
  );
};

export default Navbar;