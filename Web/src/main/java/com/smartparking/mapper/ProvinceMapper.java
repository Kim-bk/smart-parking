package com.smartparking.mapper;

import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import com.smartparking.dto.ProvinceDTO;
import com.smartparking.entity.ProvinceEntity;

@Component
public class ProvinceMapper {
	
	@Autowired
	private ModelMapper mapper;
	
	public ProvinceEntity ToEntity(ProvinceDTO dto) {
		ProvinceEntity entity = mapper.map(dto, ProvinceEntity.class);
		return entity;
		
	}
	
	public ProvinceDTO ToDTO(ProvinceEntity entity) {
		ProvinceDTO dto = mapper.map(entity, ProvinceDTO.class);
		return dto;
		
	}

}
