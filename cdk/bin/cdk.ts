#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { EssayStack } from '../lib/essay_stack';

const app = new cdk.App();

const essayStack = new EssayStack(app, 'EssayStack', {
  env: {
    account: '617503825053',
    region: 'us-west-1',
  }
});
app.synth();
