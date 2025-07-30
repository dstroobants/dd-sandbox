FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build

WORKDIR /Hello
# Copy everything
COPY Hello/ ./
# Restore as distinct layers
RUN dotnet restore
# Build and publish a release
RUN dotnet publish -o out

# Build runtime image
FROM mcr.microsoft.com/dotnet/aspnet:9.0
WORKDIR /Hello
COPY --from=build /Hello/out .
ENTRYPOINT ["dotnet", "DotNet.Docker.dll"]