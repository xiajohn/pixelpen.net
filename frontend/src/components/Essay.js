import React from 'react';
import styles from '../css/Essay.module.css';

function Essay({content}) {
  return (
    <div className={styles.essay}>
      <h2>Essay</h2>
      <p>{content}</p>
    </div>
  );
}

export default Essay;
