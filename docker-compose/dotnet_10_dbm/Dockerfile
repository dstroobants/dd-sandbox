FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build

WORKDIR /Hello
# Copy everything
COPY Hello/ ./
# Restore as distinct layers
RUN dotnet restore
# Build and publish a release
RUN dotnet publish -o out

# Build runtime image
FROM mcr.microsoft.com/dotnet/sdk:10.0

RUN apt-get update && apt-get install -y curl

# Install Datadog APM
# Download and install the Tracer
RUN mkdir -p /opt/datadog \
    && mkdir -p /var/log/datadog \
    && TRACER_VERSION=$(curl -s https://api.github.com/repos/DataDog/dd-trace-dotnet/releases/latest | grep tag_name | cut -d '"' -f 4 | cut -c2-) \
    && ARCH=$(dpkg --print-architecture) \
    && curl -LO https://github.com/DataDog/dd-trace-dotnet/releases/download/v${TRACER_VERSION}/datadog-dotnet-apm_${TRACER_VERSION}_${ARCH}.deb \
    && dpkg -i ./datadog-dotnet-apm_${TRACER_VERSION}_${ARCH}.deb \
    && rm ./datadog-dotnet-apm_${TRACER_VERSION}_${ARCH}.deb

# Enable the tracer
ENV CORECLR_ENABLE_PROFILING=1
ENV CORECLR_PROFILER={846F5F1C-F9AE-4B07-969E-05C26BC060D8}
ENV CORECLR_PROFILER_PATH=/opt/datadog/Datadog.Trace.ClrProfiler.Native.so
ENV DD_DOTNET_TRACER_HOME=/opt/datadog
ENV DD_AGENT_HOST=datadog-agent
ENV DD_AGENT_PORT=8126

WORKDIR /Hello
COPY --from=build /Hello/out .
ENTRYPOINT ["dotnet", "DotNet.Docker.dll"]
