import React from 'react'
import { PageHeader } from 'antd';

export default function Header(props) {
  return (
    <div onClick={()=>{
      window.open("https://github.com/austintgriffith/scaffold-eth");
    }}>
      <PageHeader
        title="!PiedPiper"
        subTitle="Upload their videos in the public domain while maintaining privacy."
        style={{cursor:'pointer'}}
      />
    </div>
  );
}
