FROM debian:bullseye

# add pulseaudio-utils for pacat
RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    dirmngr \
    gnupg \
    libasound2 \
    libdbus-glib-1-2 \
    libgtk-3-0 \
    libgl1-mesa-dri \
    libgl1-mesa-glx -y\
    ffmpeg \
    libsm6 \
    libxext6 -y \
    libxrender1 \
    libxtst6 \
    libx11-xcb-dev \
    libx11-xcb1 \
    libxt6 \
    libpulse0 \
    bzip2 \
    iproute2 -y \
    iputils-ping -y \
    traceroute -y \
    libcanberra-gtk-module \
    libcanberra-gtk3-module \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

ENV HOME /root

ENV LANG C.UTF-8

#https://download-installer.cdn.mozilla.net/pub/firefox/releases/
ENV FIREFOX_VERSION 124.0.1
ENV FIREFOX_LANG pt-BR

RUN cd /tmp \
    && curl -sSOL "https://download-installer.cdn.mozilla.net/pub/firefox/releases/${FIREFOX_VERSION}/linux-x86_64/${FIREFOX_LANG}/firefox-${FIREFOX_VERSION}.tar.bz2" \
    && tar -vxj -C /opt -f firefox-${FIREFOX_VERSION}.tar.bz2 \
    && rm -rf firefox-${FIREFOX_VERSION}.tar.bz2

# good fonts
COPY local.conf /etc/fonts/local.conf

WORKDIR $HOME

USER root

ENTRYPOINT [ "/opt/firefox/firefox" ]