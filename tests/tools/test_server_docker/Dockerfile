FROM linuxserver/openssh-server


RUN addgroup -S sshgroup && adduser -S sshuser -G sshgroup

USER sshuser
RUN mkdir -p /home/sshuser/.ssh && \
    chmod 0700 /home/sshuser/.ssh

COPY keys/id_rsa.pub /home/adduser/.ssh/authorized_keys
USER root
