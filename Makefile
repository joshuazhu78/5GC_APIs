API_NAME	?= AsSessionWithQoS
API_DEF		?= TS29122_AsSessionWithQoS.yaml

$(API_NAME): $(API_DEF)
	openapi-generator-cli generate \
			-i $< \
			-g go \
				--package-name=models \
			-o $@ \

clean:
	rm -rf $(API_NAME)

