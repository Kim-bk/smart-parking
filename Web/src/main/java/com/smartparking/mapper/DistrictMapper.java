package com.smartparking.mapper;

import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import com.smartparking.dto.DistrictDTO;
import com.smartparking.entity.DistrictEntity;
import com.smartparking.service.impl.ProvinceService;


@Component
public class DistrictMapper {

	@Autowired
	private ModelMapper mapper;
	
	@Autowired
	private ProvinceService provinceService;
	
	@Autowired
	private ProvinceMapper provinceMapper;
	
	public DistrictDTO toDTO(DistrictEntity entity) {
		DistrictDTO dto = mapper.map(entity, DistrictDTO.class);
		dto.setIdProvince(entity.getIdProvince());
		return dto;
	}
	
	public DistrictEntity toEntity(DistrictDTO dto) {
		DistrictEntity entity = mapper.map(dto, DistrictEntity.class);
		entity.setProvince(provinceMapper.ToEntity(provinceService.findOneById(dto.getIdProvince())));
		return entity;
	}
}
