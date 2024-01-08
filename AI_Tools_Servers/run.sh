#!/bin/bash

cd /workspace/AI_Tools_Servers && CUDA_VISIBLE_DEVICES=0 nohup python manage_ai_tools_servers.py >/dev/null 2>&1 &
